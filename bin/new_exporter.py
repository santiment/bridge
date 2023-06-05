#####This is a new file#####
"""
Provide constants to be used in stargate exporter
"""

############## ADDRESSES ##############

Router = "0x8731d54E9D02c286767d56ac03e8037C07e01e98".lower()
ETH_Router = "0x150f94B44927F078737562f0fcF3C95c01Cc2376".lower()

############## SIGNATURES ##############
# swap sig
SWAP_SIG = "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f".lower()
# send credits sig
SEND_CREDITS_SIG = "0x6939f93e3f21cf1362eb17155b740277de5687dae9a83a85909fd71da95944e7".lower()

# Swap: user_address -> Router
# SendCredits: Router -> user_address
#####This is a new file#####
"""
Provide functions for clickhouse query in stargate exporter
"""

from lib.constants import ETH_EVENTS_TABLE


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_events_v2 table using stargate contracts
    """

    query_string = f"""
    SELECT 
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index,
        CASE 
            WHEN signature = '{SWAP_SIG}' THEN 'swap'
            WHEN signature = '{SEND_CREDITS_SIG}' THEN 'send_credits'
        END as action,
        CASE 
            WHEN signature = '{SWAP_SIG}' THEN 'eth'
            ELSE 'erc20'
        END as token_type
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr IN ['{Router}', '{ETH_Router}']
        AND signature IN ['{SWAP_SIG}', '{SEND_CREDITS_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string

#####This is a new file#####
"""
Provide process function that could keep the required data in CH table format
"""

import json
from datetime import datetime
from itertools import repeat
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM, BSC
from lib.stargate.constants import Router, ETH_Router, SWAP_SIG, SEND_CREDITS_SIG

def process(project_name, records):
    """Process the records to have a standard output"""
    event_dicts = map_events_to_dictionary(project_name, records)
    processed = generate_structured_records(event_dicts)
    processed = add_computed_at(processed, datetime.now())
    logged_events = log_iter(processed, LOG_FREQUENCY, stop_early=False)

    return logged_events

def map_args(event, project_name):
    """ Map the query result from event table for stargate."""
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
    args_dict = event["args"]
    action = event["action"]
    token_type = event["token_type"]

    #Fill chain_in and chain_out based on action
    if action == "swap":
        chain_in, chain_out = ETHEREUM, BSC
    elif action == "send_credits":
        chain_in, chain_out = BSC, ETHEREUM

    #Fill token_in and token_out based on token_type
    if token_type == "eth":
        token_in, token_out = ETHEREUM, ETHEREUM

        if action == "swap":
            amount_in, amount_out = args_dict["amountSD"], args_dict["eqReward"]
            user = args_dict["from"]
        elif action == "send_credits":
            amount_in, amount_out = args_dict["credits"], args_dict["idealBalance"]
            user = args_dict["to"]

    elif token_type == "erc20":
        token_in, token_out = args_dict["tokenIn"], args_dict["tokenOut"]
        amount_in, amount_out = args_dict["amountIn"], args_dict["amountOut"]
        user = args_dict["from"]

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

#####This is a new file#####
"""Stargate Exporter Class"""
import logging
from lib.exporter import Exporter
from lib.stargate.query import build_events_query
from lib.stargate.process import process

class StargateExporter(Exporter):
    """
    Stargate Exporter Class, used to export transactions
    between ethereum and BSC.
    """
    def __init__(self):
        super().__init__()
        self.name = "stargate"

    def read_records(self):
        """
        Read data from clickhouse

        Return: records after clickhouse client execution
        """
        event_query = build_events_query(self.start_dt, self.end_dt)
        event_records = self.read_ch_client.execute(event_query)
        return event_records

    def run(self):
        """The main function to run the Stargate exporter"""

