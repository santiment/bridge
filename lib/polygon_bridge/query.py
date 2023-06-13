"""
Provide functions for clickhouse query in polygon_bridge exporter
"""

from lib.constants import ETH_TRANSFERS_TABLE, ERC20_TRANSFERS_TABLE
from lib.polygon_bridge.constants import (
    POLYGON_ERC20_BRIDGE,
    POLYGON_ETHER_BRIDGE,
    POLYGON_BRIDGE
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_transfers and erc20_transfers table using bridge protoccol contracts
    """

    query_string = f"""
    SELECT 
        transactionHash as tx_hash,
        from as user,
        value,
        dt,
        'eth' as token,
        'deposit' as action
    FROM
        {ETH_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND to = '{POLYGON_BRIDGE}'
    UNION ALL
    SELECT 
        transactionHash as tx_hash,
        to as user,
        value,
        dt,
        'eth' as token,
        'withdraw' as action
    FROM
        {ETH_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND from = '{POLYGON_ETHER_BRIDGE}'
    UNION ALL
    SELECT 
        transactionHash as tx_hash,
        from as user,
        value,
        dt, 
        contract as token,
        'deposit' as action
    FROM
        {ERC20_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND to = '{POLYGON_ERC20_BRIDGE}'

    UNION ALL
    SELECT 
        transactionHash as tx_hash,
        to as user,
        value,
        dt,
        contract as token,
        'withdraw' as action
    FROM
        {ERC20_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND from = '{POLYGON_ERC20_BRIDGE}'
    """
    return query_string
