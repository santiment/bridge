"""
Provide process function that could keep the required data in CH table format
"""

import json
from datetime import datetime
from itertools import repeat
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM, ARBITRUM_ONE
from lib.arbitrum_one.constants import ARB_BRIDGE

def process(project_name, records):
    """Process the records to have a standard output"""
    event_dicts = map_events_to_dictionary(project_name, records)
    processed = generate_structured_records(event_dicts)
    processed = add_computed_at(processed, datetime.now())
    logged_events = log_iter(processed, LOG_FREQUENCY, stop_early=False)

    return logged_events

def map_args(event, project_name):
    """ Map the query result from event table and transfers table for arb bridge."""
    # results from eth_events_v2 table
    EVENT_QUERY_LENGTH = 5
    if len(event) > EVENT_QUERY_LENGTH:
        args_dict = json.loads(event[2])

        return {
            "tx_hash": event[0],
            "contract_address": event[1],
            "dt": event[3],
            "log_index": event[4],
            "action": event[5],
            "token_type": event[6],
            "project_name": project_name,
            "args": args_dict,
        }

    # results from eth_transfers table
    return {
        "tx_hash": event[0],
        "contract_address": ARB_BRIDGE,
        "dt": event[1],
        "log_index": 0,
        "action": "deposit",
        "token_type": "eth",
        "project_name": project_name,
        "from": event[2],
        "value": event[3]
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
    args_dict = None
    action = event["action"]
    token_type = event["token_type"]


    #Fill chain_in and chain_out based on action
    if action == "withdraw":
        chain_in, chain_out = ETHEREUM, ARBITRUM_ONE
    elif action == "deposit":
        chain_in, chain_out = ARBITRUM_ONE, ETHEREUM

    #Fill token_in and token_out based on token_type
    if token_type == "eth":
        token_in, token_out = ETHEREUM, ETHEREUM

        if action == "withdraw":
            args_dict = event["args"]
            eth_amount = int(args_dict["value"])
            if eth_amount == 0:
                return None
            amount_in, amount_out = eth_amount, eth_amount
            user = args_dict["to"]
        elif action == "deposit":
            amount_in, amount_out = int(event["value"]), int(event["value"])
            user = event["from"]


    elif token_type == "erc20":
        args_dict = event["args"]
        token_in, token_out = args_dict["l1Token"], args_dict["l1Token"]
        amount_in, amount_out = int(args_dict["_amount"]), int(args_dict["_amount"])
        user = args_dict["_from"]

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
