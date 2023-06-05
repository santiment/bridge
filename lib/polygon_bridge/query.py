"""
Provide functions for clickhouse query in polygon_bridge exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.polygon_bridge.constants import (
    POLYGON_BRIDGE,
    LOCKED_ERC20_SIG,
    LOCKED_ETHER_SIG,
    EXITED_ETHER_SIG
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
            WHEN signature = '{LOCKED_ERC20_SIG}' THEN 'LockedERC20'
            WHEN signature = '{LOCKED_ETHER_SIG}' THEN 'LockedEther'
            WHEN signature = '{EXITED_ETHER_SIG}' THEN 'ExitedEther'
        END as action
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{POLYGON_BRIDGE}'
        AND signature IN ['{LOCKED_ERC20_SIG}', '{LOCKED_ETHER_SIG}', '{EXITED_ETHER_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    print (query_string)
    return query_string
