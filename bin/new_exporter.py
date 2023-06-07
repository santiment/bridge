#####This is a new file#####
"""
Provide constants to be used in polygon_bridge exporter
"""

############## ADDRESSES ##############

POLYGON_ERC20_BRIDGE = "0x40ec5B33f54e0E8A33A975908C5BA1c14e5BbbDf".lower()
POLYGON_ETHER_BRIDGE = "0x8484Ef722627bf18ca5Ae6BcF031c23E6e922B30".lower()

############## SIGNATURES ##############

TRANSFER_EVENT_SIG = "0xa9059cbb000000000000000000000000"
#####This is a new file#####
"""
Provide functions for clickhouse query in polygon_bridge exporter
"""

from lib.constants import ETH_TRANSFERS_TABLE, ERC20_TRANSFERS_TABLE
from lib.polygon_bridge.constants import (
    POLYGON_ERC20_BRIDGE,
    POLYGON_ETHER_BRIDGE,
    TRANSFER_EVENT_SIG
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_transfers and erc20_transfers table using bridge protoccol contracts
    """

    query_string = f"""
    SELECT 
        transactionHash as tx_hash,
        contract as contract_address,
        to as user,
        value,
        dt
    FROM
        {ETH_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract = '{POLYGON_ETHER_BRIDGE}'
    UNION ALL
    SELECT 
        transactionHash as tx_hash,
        contract as contract_address,
        to as user,
        value,
        dt
    FROM
        {ERC20_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract = '{POLYGON_ERC20_BRIDGE}'
        AND left(input, 10) = '{TRANSFER_EVENT_SIG}'
    """
    return query_string
#####This is a new file#####
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

**********
1. Module and project name: polygon_bridge
2. You have to separate each output file using "#####This is a new file#####\n"
3. Some useful addresses: POLYGON_ERC20_BRIDGE = "0x40ec5B33f54e0E8A33A975908C5BA1c14e5BbbDf".lower(), 
POLYGON_ETHER_BRIDGE = "0x8484Ef722627bf18ca5Ae6BcF031c23E6e922B30".lower()
4. You should track the ERC20 token and ETH using Santiment tables: `erc20_transfers` and `eth_transfers`.
5. erc20_transfers table include following columns: {"dt", "from", "to", "value", "contract", "transactionHash"} etc.
6. The output database table schema should be reflected in the `build_event` function in the `process.py` file.
The output dictionary must contain the field like:
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
    "args": args_string,
    "computed_at": None
}

