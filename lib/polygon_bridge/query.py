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
        transactionHash AS tx_hash,
        from AS user,
        value,
        dt,
        'eth' AS token,
        if(to='{POLYGON_BRIDGE}', 'deposit', 'withdraw') AS action
    FROM
        {ETH_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND ( to = '{POLYGON_BRIDGE}' or from = '{POLYGON_ETHER_BRIDGE}')
    UNION ALL
    SELECT 
        transactionHash AS tx_hash,
        from AS user,
        value,
        dt, 
        contract AS token,
        if(to='{POLYGON_ERC20_BRIDGE}', 'deposit', 'withdraw') AS action
    FROM
        {ERC20_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND ( to = '{POLYGON_ERC20_BRIDGE}' or from = '{POLYGON_ERC20_BRIDGE}')
    """
    return query_string
