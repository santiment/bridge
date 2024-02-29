"""
Provide process function that could keep the required data in CH table format
"""

import json
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM, AVALANCHE


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
            "dt": event[0],
            "tx_hash": event[1],
            "from": event[2],
            "to": event[3],
            "amount": int(event[4]),
            "token": event[5],
            "action": event[6],
            "project_name": project_name
        }

    return map(map_args, events)


def build_event(event):
    """
    Referenced in process function, the event would be formatted as the bridge_transactions table.
    """
    action, token = event["action"], event["token"]
    if action == "deposit":
        chain_in, chain_out = AVALANCHE, ETHEREUM
        user = event['from']
    elif action == "withdraw":
        chain_in, chain_out = ETHEREUM, AVALANCHE
        user = event['to']
    else:
        raise RuntimeError("The event contains an invalid action")

    event_dict = {
        "tx_hash": event["tx_hash"],
        "log_index": 0,
        "dt": event["dt"],
        "chain_in": chain_in,
        "chain_out": chain_out,
        "contract_addr": token,
        "token_in": token,
        "token_out": token,
        "amount_in": event["amount"],
        "amount_out": event["amount"],
        "project_name": event["project_name"],
        "user": user,
        "args": json.dumps({}),
        "computed_at": None
    }
    return event_dict

def generate_structured_records(events):
    """Generator for structred events"""
    for event in events:
        yield build_event(event)
