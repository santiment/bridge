"""
Provide process function that could keep the required data in CH table format
"""

import json
import logging
from datetime import datetime
from itertools import repeat
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM
from lib.stargate.constants import CHAIN_DICT

def process(project_name, records):
    """Process the records to have a standard output"""
    event_dicts = map_events_to_dictionary(project_name, records)
    processed = generate_structured_records(event_dicts)
    processed = add_computed_at(processed, datetime.now())
    logged_events = log_iter(processed, LOG_FREQUENCY, stop_early=False)

    return logged_events

def map_args(event, project_name):
    """ Map the query result from event table for stargate."""
    args_dict = json.loads(event[2])

    return {
        "tx_hash": event[0],
        "contract_address": event[1],
        "dt": event[3],
        "log_index": event[4],
        "action": event[5],
        "project_name": project_name,
        "args": args_dict,
        "withdraw_args": json.loads(event[6]) if event[6] else ""
    }

def map_events_to_dictionary(project_name, events):
    """
    Extract the eth-events into a python dictionary
    """

    return map(map_args, events, repeat(project_name))


def build_event(event):
    """
    Referenced in process function, the event would be formatted as the bridge_transactions table.
    :param event: event dict from eth_events_v2 table
    :param with_args: whether to include args in event dictionary
    """
    args_dict = event["args"]
    action = event["action"]
    
    token_in, token_out = event["contract_address"], event["contract_address"]
    amount_in, amount_out = args_dict["amountSD"], args_dict["amountSD"]
    if action == "deposit":
        user = args_dict["from"]
        chain_id = args_dict["chainId"]
        chain_in, chain_out = ETHEREUM, get_chain(chain_id)
    elif action == "withdraw":
        user = args_dict["to"]
        chain_id = event["withdraw_args"]["chainId"]
        chain_in, chain_out = get_chain(chain_id), ETHEREUM
    
    args_string = json.dumps(args_dict) if args_dict else ""
    event_dict = {
        "tx_hash": event["tx_hash"],
        "log_index": event["log_index"],
        "dt": event["dt"],
        "chain_in": chain_in,
        "chain_out": chain_out,
        "contract_addr": event["contract_address"],
        "token_in": token_in,
        "token_out": token_out,
        "amount_in": amount_in,
        "amount_out": amount_out,
        "project_name": event["project_name"],
        "user": user,
        "args": args_string,
        "computed_at": None
    }
    return event_dict

def generate_structured_records(events):
    """Generator for structred events"""
    for event in events:
        structured = build_event(event)
        if structured:
            yield structured

def get_chain(chain_id):
    """Get chain name based on chain id provided in event args"""
    if chain_id not in CHAIN_DICT:
        logging.info("ChainId %s not found in stored dict!", chain_id)
        return chain_id
    return CHAIN_DICT[chain_id]