"""
Provide functions for clickhouse query in stargate exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.stargate.constants import (
    SWAP_SIG,
    SEND_CREDITS_SIG,
    ROUTER,
    ETH_ROUTER
)


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
        END as action
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND signature IN ['{SWAP_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    print (query_string)
    return query_string

