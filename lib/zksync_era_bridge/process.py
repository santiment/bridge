"""
Provide process function that could keep the required data in CH table format
"""

import json
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM, ZKSYNC
from lib.zksync_era_bridge.constants import ZKSYNC_DIAMOND_PROXY

def process(project_name, records):
    """Process the records to have a standard output"""
    event_dicts = map_events_to_dictionary(project_name, records)
    processed = generate_structured_records(event_dicts)
    processed = add_computed_at(processed, datetime.now())
    logged_events = log_iter(processed, LOG_FREQUENCY, stop_early=False)

    return logged_events


def map_events_to_dictionary(project_name, events):
    """
    Extract the eth-events into a python dictionary
    """

    def map_args(event):
        event_query_length = 5
        if len(event) == event_query_length:
            # eth deposit from eth_transfers table
            return {
                "tx_hash": event[0],
                "dt": event[1],
                "from": event[2],
                "value": event[3],
                "action": event[4],
                "args" : {},
                "log_index": 0,
                "contract_address": ZKSYNC_DIAMOND_PROXY,
                "project_name": project_name
            }
        args_dict = json.loads(event[2])

        return {
            "tx_hash": event[0],
            "contract_address": event[1],
            "args": args_dict,
            "dt": event[3],
            "log_index": event[4],
            "action": event[5],
            "project_name": project_name
        }

    return map(map_args, events)


def build_event(event):
    """
    Referenced in process function, the event would be formatted as the bridge_transactions table.
    :param event: event dict from eth_events_v2 table
    :param with_args: whether to include args in event dictionary
    """
    args_dict = event["args"]
    action = event["action"]

    if action == "eth_deposit":
        chain_in, chain_out = ETHEREUM, ZKSYNC
        token_in, token_out = ETHEREUM, ETHEREUM
        amount_in, amount_out = int(event["value"]), int(event["value"])
        user = event["from"]

    elif action == "eth_withdraw":
        chain_in, chain_out = ZKSYNC, ETHEREUM
        token_in, token_out = ETHEREUM, ETHEREUM
        amount_in, amount_out = int(args_dict["amount"]), int(args_dict["amount"])
        user = args_dict["to"]

    elif action == "deposit":
        chain_in, chain_out = ETHEREUM, ZKSYNC
        token_in, token_out = args_dict["l1Token"], args_dict["l1Token"]
        amount_in, amount_out = int(args_dict["amount"]), int(args_dict["amount"])
        user = args_dict["from"]

    elif action == "withdraw":
        chain_in, chain_out = ZKSYNC, ETHEREUM
        token_in, token_out = args_dict["l1Token"], args_dict["l1Token"]
        amount_in, amount_out = int(args_dict["amount"]), int(args_dict["amount"])
        user = args_dict["to"]

    else:
        raise RuntimeError("The event contains an invalid action")

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
        "args": json.dumps(args_dict),
        "computed_at": None
    }
    return event_dict

def generate_structured_records(events):
    """Generator for structred events"""
    for event in events:
        yield build_event(event)
