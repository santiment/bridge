"""
Provide process function that could keep the required data in CH table format
"""

import json
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM, OPTIMISIM
from lib.op_bridge.constants import OP_BRIDGE


def process(project_name, records):
    """Process the records to have a standard output"""
    event_dicts = map_events_to_dictionary(project_name, records)
    processed = generate_structured_records(event_dicts)
    processed = add_computed_at(processed, datetime.now())
    logged_events = log_iter(processed, LOG_FREQUENCY, stop_early=False)

    return logged_events


def map_events_to_dictionary(project_name, events):
    """
    Extract the eth-transfers and erc20-transfers into a python dictionary
    """

    def map_args(event):
        return {
            "tx_hash": event[0],
            "user": event[1],
            "amount": int(event[2]),
            "dt": event[3],
            "token": event[4],
            "action": event[5],
            "project_name": project_name
        }

    return map(map_args, events)


def build_event(event):
    """
    Referenced in process function, the event would be formatted as the bridge_transactions table.
    :param event: event dict from eth_transfers and erc20_transfers table
    """
    action, token_type = event["action"], event["token_type"]
    args = event["args"]
    user, amount = args["from"], args["amount"]
    if action == "deposit":
        chain_in, chain_out = ETHEREUM, OPTIMISIM
    elif action == "withdraw":
        chain_in, chain_out = OPTIMISIM, ETHEREUM
    else:
        raise RuntimeError("The event contains an invalid action")
    
    if token_type == "eth":
        token = ETHEREUM
    else:
        token = args["l1Token"]

    event_dict = {
        "tx_hash": event["tx_hash"],
        "log_index": event["log_index"],
        "dt": event["dt"],
        "chain_in": chain_in,
        "chain_out": chain_out,
        "contract_addr": OP_BRIDGE,
        "token_in":token,
        "token_out": token,
        "amount_in": amount,
        "amount_out": amount,
        "project_name": event["project_name"],
        "user": user,
        "args": args,
        "computed_at": None
    }
    return event_dict

def generate_structured_records(events):
    """Generator for structred events"""
    for event in events:
        yield build_event(event)
