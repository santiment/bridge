"""
Provide process function that could keep the required data in CH table format
"""
import json
import logging
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY
from lib.across.constants import (
    ACROSS_BRIDGE,
    chain_id,
    FUNDS_DEPOSIT_SIG
)

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
            "contract_addr": event[1],
            "args": event[2],
            "dt": event[3],
            "log_index": event[4],
            "signature": event[5],
            "project_name": project_name
        }

    return map(map_args, events)


def build_event(event):
    """
    Referenced in process function, the event would be formatted as the bridge_transactions table.
    :param event: event dict from eth_transfers and erc20_transfers table
    """
    args = json.loads(event["args"])
    signature = event["signature"]
    amount = int(args["amount"])
    in_id, out_id = args["originChainId"], args["destinationChainId"]
    # Get chain info from chain_id.json
    try:
        chain_in, chain_out = chain_id[in_id], chain_id[out_id]
    except KeyError as key_error:
        logging.info("Chain id %s / %s missing in chain_id.json!", in_id, out_id)
        logging.error(key_error)
        raise KeyError("Chain ids are missing in chain_id.json!") from key_error

    if signature == FUNDS_DEPOSIT_SIG:
        token = args["originToken"]
        user = args["depositor"]
    else:
        token = args["destinationToken"]
        user = args["recipient"]

    event_dict = {
        "tx_hash": event["tx_hash"],
        "log_index": event["log_index"],
        "dt": event["dt"],
        "chain_in": chain_in,
        "chain_out": chain_out,
        "contract_addr": ACROSS_BRIDGE,
        "token_in":token,
        "token_out": token,
        "amount_in": amount,
        "amount_out": amount,
        "project_name": event["project_name"],
        "user": user,
        "args": json.dumps(args),
        "computed_at": None
    }
    return event_dict

def generate_structured_records(events):
    """Generator for structred events"""
    for event in events:
        yield build_event(event)
