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
