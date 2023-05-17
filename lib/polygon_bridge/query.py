"""
Provide functions for clickhouse query in polygon bridge exporter
"""

from lib.constants import ETH_TRANSFERS_TABLE, ERC20_TRANSFERS_TABLE
from lib.polygon_bridge.constants import (
    POLYGON_BRIDGE,
    POLYGON_ETHER_BRIDGE
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
        {ETH_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{WBTC_FACTORY}'
        AND signature IN ['{MINT_CONFIRMED_SIG}', '{BURNED_CONFIRMED_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string
