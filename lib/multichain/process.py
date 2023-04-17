"""
Provide process function that could keep the required data in CH table format
"""

import json
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM
from lib.multichain.constants import chain_info

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
            "contract_addr": event[1],
            "dt": event[3],
            "log_index": event[4],
            "action": event[5],
            "project_name": project_name,
            "args": args_dict,
            "transfer_contract": event[6],
        }

    return map(map_args, events)

def get_chain(chain_id):
    """Get the chain name from chain id"""
    try:
        return chain_info[chain_id]["name"].lower()
    # pylint: disable=broad-except
    except Exception:
        return chain_id

def build_event(event):
    """
    Referenced in process function, the event would be formatted as the bridge_transactions table.
    :param event: event dict from eth_events_v2 table
    :param with_args: whether to include args in event dictionary
    """
    args_dict = event["args"]
    action = event["action"]
    amount = int(args_dict["amount"])
    amount_in, amount_out = amount, amount

    if action == "swap_in":
        chain_id = args_dict["fromChainID"]
        user = args_dict["to"]
        chain_in, chain_out = get_chain(chain_id), ETHEREUM
        token_in, token_out = args_dict["token"], event["transfer_contract"]

    elif action == "swap_out":
        chain_id = args_dict["toChainID"]
        user = args_dict["from"]
        chain_in, chain_out = ETHEREUM, get_chain(chain_id)
        token_in, token_out = event["transfer_contract"], args_dict["token"]
    else:
        raise RuntimeError("The event contains an invalid action")

    event_dict = {
        "tx_hash": event["tx_hash"],
        "log_index": event["log_index"],
        "dt": event["dt"],
        "chain_in": chain_in,
        "chain_out": chain_out,
        "contract_addr": event["contract_addr"],
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
