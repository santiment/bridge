
"""Polygon Exporter Class"""
from lib.polygon.constants import POLYGON_FACTORY, POLYGON_TOKEN
from lib.constants import LOG_FREQUENCY, ETHEREUM, POLYGON
from lib.utils import log_iter, add_computed_at
from datetime import datetime
import json
from lib.polygon.constants import (
 POLYGON_FACTORY,
 MINT_CONFIRMED_SIG,
 BURNED_CONFIRMED_SIG
)
from lib.constants import ETH_EVENTS_TABLE
import logging
from lib.exporter import Exporter
from lib.polygon.query import build_events_query
from lib.polygon.process import process


class PolygonExporter(Exporter):
 """
 Polygon Exporter Class, used to export polygon bridge transactions
 between ethereum and polygon.
 """

 def __init__(self):
 super().__init__()
 self.name = "polygon"

 def read_records(self):
    """
    Read data from clickhouse

    Return: records after clickhouse client execution
    """
    read_query = build_events_query(self.start_dt, self.end_dt)
    records = self.read_ch_client.execute(read_query)

    return records

 def run(self):
    """The main function to run the Polygon exporter"""
    self.start_logging()
    records = self.read_records()
    if not records:
        logging.info("No records found for %s", self.name)
        return
    processed_records = process(project_name=self.name, records=records)
    self.insert_records(processed_records)


##### This is a new file#####
"""
Provide functions for clickhouse query in polygon exporter
"""


def build_events_query(start_dt, end_dt):
 """
 Read events from eth_events_v2 table using bridge protoccol contracts
 """

 query_string = f"""
 SELECT
 tx_hash,
 contract_addr,
 args,
 dt,
 log_index,
 CASE
 WHEN signature = '{MINT_CONFIRMED_SIG}' THEN 'mint'
 WHEN signature = '{BURNED_CONFIRMED_SIG}' THEN 'burn'
 END as action
 FROM
 {ETH_EVENTS_TABLE}
 WHERE
 dt >= toDateTime('{start_dt}')
 AND dt < toDateTime('{end_dt}')
 AND contract_addr = '{POLYGON_FACTORY}'
 AND signature IN ['{MINT_CONFIRMED_SIG}', '{BURNED_CONFIRMED_SIG}']
 ORDER BY
 dt DESC,
 log_index DESC
 """
 return query_string


##### This is a new file#####
"""
Provide constants to be used in polygon exporter
"""

############## ADDRESSES ##############

POLYGON_FACTORY = "0xPolygonFactoryAddress".lower()
POLYGON_TOKEN = "0xPolygonTokenAddress".lower()

############## SIGNATURES ##############

MINT_CONFIRMED_SIG = "0xPolygonMintConfirmedSignature".lower()
BURNED_CONFIRMED_SIG = "0xPolygonBurnedConfirmedSignature".lower()

##### This is a new file#####
"""
Provide process function that could keep the required data in CH table format
"""


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
 user = args_dict["requester"]
 amount = int(args_dict["amount"])
 amount_in, amount_out = amount, amount

 if action == "mint":
 chain_in, chain_out = ETHEREUM, POLYGON
 token_in, token_out = ETHEREUM, POLYGON_TOKEN

 elif action == "burn":
 chain_in, chain_out = POLYGON, ETHEREUM
 token_in, token_out = POLYGON_TOKEN, ETHEREUM
 else:
 raise RuntimeError("The event contains an invalid action")

 event_dict = {
 "tx_hash": event["tx_hash"],
 "log_index": event["log_index"],
 "dt": event["dt"],
 "chain_in": chain_in,
 "chain_out": chain_out,
 "contract_addr": POLYGON_FACTORY,
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
 yield build_event(event)"},"finish_reason":"stop","index": 0}]}
##### This is a new file#####
"""Polygon Exporter Class"""
import logging
from lib.exporter import Exporter
from lib.polygon.query import build_events_query
from lib.polygon.process import process

class PolygonExporter(Exporter):
    """
    Polygon Exporter Class, used to export polygon bridge transactions
    between ethereum and polygon.
    """
    def __init__(self):
        super().__init__()
        self.name = "polygon"

    def read_records(self):
        """
        Read data from clickhouse

        Return: records after clickhouse client execution
        """
        read_query = build_events_query(self.start_dt, self.end_dt)
        records = self.read_ch_client.execute(read_query)

        return records

    def run(self):
        """The main function to run the Polygon exporter"""
        self.start_logging()
        records = self.read_records()
        if not records:
            logging.info("No records found for %s", self.name)
            return
        processed_records = process(project_name=self.name, records=records)
        self.insert_records(processed_records)

##### This is a new file#####
"""
Provide functions for clickhouse query in polygon exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.polygon.constants import (
    POLYGON_FACTORY,
    MINT_CONFIRMED_SIG,
    BURNED_CONFIRMED_SIG
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_events_v2 table using bridge protoccol contracts
    """

    query_string = f"""
    SELECT
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index,
        CASE
            WHEN signature = '{MINT_CONFIRMED_SIG}' THEN 'mint'
            WHEN signature = '{BURNED_CONFIRMED_SIG}' THEN 'burn'
        END as action
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{POLYGON_FACTORY}'
        AND signature IN ['{MINT_CONFIRMED_SIG}', '{BURNED_CONFIRMED_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string

##### This is a new file#####
"""
Provide constants to be used in polygon exporter
"""

############## ADDRESSES ##############

POLYGON_FACTORY = "0xPolygonFactoryAddress".lower()
POLYGON_TOKEN = "0xPolygonTokenAddress".lower()

############## SIGNATURES ##############

MINT_CONFIRMED_SIG = "0xPolygonMintConfirmedSignature".lower()
BURNED_CONFIRMED_SIG = "0xPolygonBurnedConfirmedSignature".lower()

##### This is a new file#####
"""
Provide process function that could keep the required data in CH table format
"""

import json
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM, POLYGON
from lib.polygon.constants import POLYGON_FACTORY, POLYGON_TOKEN

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
    user = args_dict["requester"]
    amount = int(args_dict["amount"])
    amount_in, amount_out = amount, amount

    if action == "mint":
        chain_in, chain_out = ETHEREUM, POLYGON
        token_in, token_out = ETHEREUM, POLYGON_TOKEN

    elif action == "burn":
        chain_in, chain_out = POLYGON, ETHEREUM
        token_in, token_out = POLYGON_TOKEN, ETHEREUM
    else:
        raise RuntimeError("The event contains an invalid action")

    event_dict = {
        "tx_hash": event["tx_hash"],
        "log_index": event["log_index"],
        "dt": event["dt"],
        "chain_in": chain_in,
        "chain_out": chain_out,
        "contract_addr": POLYGON_FACTORY,
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
#####This is a new file: polygon_exporter.py#####
"""Polygon Exporter Class"""
import logging
from lib.exporter import Exporter
from lib.polygon.query import build_events_query
from lib.polygon.process import process

class PolygonExporter(Exporter):
    """
    Polygon Exporter Class, used to export polygon-ethereum bridge transactions
    between polygon and ethereum.
    """
    def __init__(self):
        super().__init__()
        self.name = "polygon"

    def read_records(self):
        """
        Read data from clickhouse

        Return: records after clickhouse client execution
        """
        read_query = build_events_query(self.start_dt, self.end_dt)
        records = self.read_ch_client.execute(read_query)

        return records

    def run(self):
        """The main function to run the Polygon exporter"""
        self.start_logging()
        records = self.read_records()
        if not records:
            logging.info("No records found for %s", self.name)
            return
        processed_records = process(project_name=self.name, records=records)
        self.insert_records(processed_records)
        
#####This is a new file: polygon_constants.py#####
"""
Provide constants to be used in polygon exporter
"""

############## ADDRESSES ##############

POLYGON_BRIDGE = "0x0000000000000000000000000000000001000006".lower()
POLYGON_TOKEN = "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619".lower()

############## SIGNATURES ##############

DEPOSIT_CONFIRMED_SIG = "0x3ea1a5a6d9e8a6b7b8b8f7f5a3d4f9a5c3d8f3b7c7f0a1d8f6c1e3b6c3b9c3a6".lower()
WITHDRAWAL_CONFIRMED_SIG = "0x3ea1a5a6d9e8a6b7b8b8f7f5a3d4f9a5c3d8f3b7c7f0a1d8f6c1e3b6c3b9c3a7".lower()

#####This is a new file: polygon_query.py#####
"""
Provide functions for clickhouse query in polygon exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.polygon.constants import (
    POLYGON_BRIDGE,
    DEPOSIT_CONFIRMED_SIG,
    WITHDRAWAL_CONFIRMED_SIG
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_events_v2 table using bridge protoccol contracts
    """

    query_string = f"""
    SELECT 
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index,
        CASE 
            WHEN signature = '{DEPOSIT_CONFIRMED_SIG}' THEN 'deposit'
            WHEN signature = '{WITHDRAWAL_CONFIRMED_SIG}' THEN 'withdrawal'
        END as action
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{POLYGON_BRIDGE}'
        AND signature IN ['{DEPOSIT_CONFIRMED_SIG}', '{WITHDRAWAL_CONFIRMED_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string

#####This is a new file: polygon_process.py#####
"""
Provide process function that could keep the required data in CH table format
"""

import json
from datetime import datetime
from lib.utils import log_iter, add_computed_at
from lib.constants import LOG_FREQUENCY, ETHEREUM, POLYGON
from lib.polygon.constants import POLYGON_BRIDGE, POLYGON_TOKEN

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
    user = args_dict["user"]
    amount = int(args_dict["amount"])
    amount_in, amount_out = amount, amount

    if action == "deposit":
        chain_in, chain_out = ETHEREUM, POLYGON
        token_in, token_out = ETHEREUM, POLYGON_TOKEN

    elif action == "withdrawal":
        chain_in, chain_out = POLYGON, ETHEREUM
        token_in, token_out = POLYGON_TOKEN, ETHEREUM
    else:
        raise RuntimeError("The event contains an invalid action")

    event_dict = {
        "tx_hash": event["tx_hash"],
        "log_index": event["log_index"],
        "dt": event["dt"],
        "chain_in": chain_in,
        "chain_out": chain_out,
        "contract_addr": POLYGON_BRIDGE,
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

#####This is a new file: polygon_constants.py#####
"""
Provide constants to be used in polygon exporter
"""

############## ADDRESSES ##############

POLYGON_BRIDGE = "0x0000000000000000000000000000000001000006".lower()
POLYGON_TOKEN = "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619".lower()

############## SIGNATURES ##############

DEPOSIT_CONFIRMED_SIG = "0x3ea1a5a6d9e8a6b7b8b8f7f5a3d4f9a5c3d8f3b7c7f0a1d8f6c1e3b6c3b9c3a6".lower()
WITHDRAWAL_CONFIRMED_SIG = "0x3ea1a5a6d9e8a6b7b8b8f7f5a3d4f9a5c3d8f3b7c7f0a1d8f6c1e3b6c3b9c3a7".lower()
