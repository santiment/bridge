"""
Provide process function that could keep the required data in CH table format
"""
import json
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM
from lib.squid.constants import SQUID_ROUTER


def process(project_name, records, action):
    """Process the records to have a standard output"""
    event_dicts = map_events_to_dictionary(project_name, records, action)
    processed = generate_structured_records(event_dicts)
    processed = add_computed_at(processed, datetime.now())
    logged_events = log_iter(processed, LOG_FREQUENCY, stop_early=False)

    return logged_events


def map_events_to_dictionary(project_name, events, action):
    """
    Extract the eth-transfers and erc20-transfers into a python dictionary
    @params:
        project_name: project name
        events: output of clickhouse query execution
        action: "deposit" or "withdraw"
    """

    def map_deposit(event):
        return {
            "tx_hash": event[0],
            "dt": event[1],
            "token": event[2],
            "args": event[3],
            "log_index": event[4],
            "user": event[5],
            "project_name": project_name,
            "action": "deposit"
        }

    def map_withdraw(event):
        return {
            "tx_hash": event[0],
            "dt": event[1],
            "args": event[2],
            "log_index": event[3],
            "user": SQUID_ROUTER,
            "project_name": project_name,
            "action": "withdraw"
        }

    if action == "deposit":
        return map(map_deposit, events)
    if action == "withdraw":
        return map(map_withdraw, events)


def build_event(event):
    """
    Referenced in process function, the event would be formatted as the bridge_transactions table.
    :param event: event dict from eth_transfers and erc20_transfers table
    """
    action, user = event["action"], event["user"]
    args = json.loads(event["args"])
    amount = int(args["amount"])
    if action == "deposit":
        chain_in, chain_out = ETHEREUM, args["destinationChain"]
        token = event["token"]
    else:
        chain_in, chain_out = args["sourceChain"], ETHEREUM
        token = args["symbol"]

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
