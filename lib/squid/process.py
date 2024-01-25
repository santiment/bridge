"""
Provide process function that could keep the required data in CH table format
"""
import json
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM
from lib.squid.constants import SQUID_ROUTER


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
            "dt": event[1],
            "token": event[2],
            "args": event[3],
            "log_index": event[4],
            "user": event[5],
            "project_name": project_name
        }

    return map(map_args, events)


def build_event(event):
    """
    Referenced in process function, the event would be formatted as the bridge_transactions table.
    :param event: event dict from eth_transfers and erc20_transfers table
    """
    args = json.loads(event["args"])
    token, amount = event["token"], int(args["amount"])
    chain_in, chain_out = ETHEREUM, args["destinationChain"]
    user = event["user"]

    event_dict = {
        "tx_hash": event["tx_hash"],
        "log_index": event["log_index"],
        "dt": event["dt"],
        "chain_in": chain_in,
        "chain_out": chain_out,
        "contract_addr": SQUID_ROUTER,
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
