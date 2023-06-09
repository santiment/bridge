"""
Provide process function that could keep the required data in CH table format
"""

import json
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM, POLYGON
from lib.polygon_bridge.constants import POLYGON_ERC20_BRIDGE, POLYGON_ETHER_BRIDGE


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
        contract_address = event[1]
        if contract_address == POLYGON_ETHER_BRIDGE:
            token_in = ETHEREUM
            chain_in = ETHEREUM
            chain_out = POLYGON
            token_out = POLYGON_ERC20_BRIDGE
        elif contract_address == POLYGON_ERC20_BRIDGE:
            token_in = event[1]
            chain_in = POLYGON
            chain_out = ETHEREUM
            token_out = ETHEREUM
        else:
            raise RuntimeError("The event contains an invalid contract address")

        return {
            "tx_hash": event[0],
            "contract_address": contract_address,
            "user": event[2],
            "amount": int(event[3]),
            "dt": event[4],
            "project_name": project_name,
            "token_in": token_in,
            "chain_in": chain_in,
            "chain_out": chain_out,
            "token_out": token_out,
        }

    return map(map_args, events)


def build_event(event):
    """
    Referenced in process function, the event would be formatted as the bridge_transactions table.
    :param event: event dict from eth_transfers and erc20_transfers table
    """
    event_dict = {
        "tx_hash": event["tx_hash"],
        "dt": event["dt"],
        "chain_in": event["chain_in"],
        "chain_out": event["chain_out"],
        "contract_addr": event["contract_address"],
        "token_in": event["token_in"],
        "token_out": event["token_out"],
        "amount_in": event["amount"],
        "amount_out": event["amount"],
        "project_name": event["project_name"],
        "user": event["user"],
        "args": json.dumps({}),
        "computed_at": None
    }
    return event_dict


def generate_structured_records(events):
    """Generator for structred events"""
    for event in events:
        yield build_event(event)