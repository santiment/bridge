"""
Provide constants to be used in exporters
"""

import os
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
WRITE_CHUNK_SIZE = 10_000


def parse_iso_time(day_str):
    """Parse iso format as needed"""
    return datetime.fromisoformat(day_str).strftime(DATE_FORMAT)


def before_days(days):
    """Return the iso format of timedelta of days"""
    dt_delta = datetime.now() - timedelta(days=days)
    return dt_delta.isoformat()


DRY_RUN = int(os.getenv("DRY_RUN", "0"))

CH_HOST = os.getenv("CH_HOST", "clickhouse.stage.san")
CH_PORT = int(os.getenv("CH_PORT", "30900"))
READ_CHUNK_SIZE = 100_000
WRITE_CHUNK_SIZE = 10_000

start_default = before_days(900)
end_default = before_days(890)
START_DT = parse_iso_time(os.getenv("START_DT", start_default))
END_DT = parse_iso_time(os.getenv("END_DT", end_default))


LOG_FORMAT = os.getenv("LOG_FORMAT", '{"level": "%(levelname)s", "time": "%(asctime)s", "message": "%(message)s"}')
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

############## TABLES ##############

ETH_EVENTS_TABLE = os.getenv("ETH_EVENTS_TABLE", "eth_events_v2")
ETH_RECEIPTS_TABLE = os.getenv("ETH_RECEIPTS_TABLE", "eth_receipts")
BRIDGE_TRANSACTIONS_TABLE = os.getenv("BRIDGE_TRANSACTIONS_TABLE", "bridge_transactions")
ERC20_TRANSFERS_TABLE = os.getenv("ERC20_TRANSFERS_TABLE", "erc20_transfers")
ETH_TRANSFERS_TABLE = os.getenv("ETH_TRANSFERS_TABLE", "eth_transfers")

############## ADDRESSES ##############

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

############## CHAIN ##############
ETHEREUM, BITCOIN = "ethereum", "bitcoin"