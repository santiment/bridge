"""
Provide process function that could keep the required data in CH table format
"""

import json
import logging
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM, ZKSYNC
from lib.zksync_lite.constants import TOKEN_DICT, ZKSYNC_LITE

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
        args_dict = json.loads(event[2])

        return {
            "tx_hash": event[0],
            "pool_address": event[1],
            "dt": event[3],
            "log_index": event[4],
            "action": event[5],
            "project_name": project_name,
            "args": args_dict,
            "from": event[6]
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
    token_id = int(args_dict["tokenId"])
    amount = int(args_dict["amount"])
    amount_in, amount_out = amount, amount
    try:
        token_in, token_out = TOKEN_DICT[token_id], TOKEN_DICT[token_id]
    except KeyError as key_error:
        logging.info(key_error)
        token_in, token_out = None, None

    if action == "withdraw":
        chain_in, chain_out = ZKSYNC, ETHEREUM
        user = args_dict["owner"]
    elif action == "deposit":
        chain_in, chain_out = ETHEREUM, ZKSYNC
        user = event["from"]
    else:
        raise RuntimeError("The event contains an invalid action")

    event_dict = {
        "tx_hash": event["tx_hash"],
        "log_index": event["log_index"],
        "dt": event["dt"],
        "chain_in": chain_in,
        "chain_out": chain_out,
        "contract_addr": ZKSYNC_LITE,
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
