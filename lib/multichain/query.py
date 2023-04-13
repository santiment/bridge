"""
Provide functions for clickhouse query in multichain exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.multichain.constants import (
    SWAP_IN_SIG,
    SWAP_OUT_SIG1,
    SWAP_OUT_SIG2
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_events_v2 table using the lending pools contract
    and the signature corresponding to borrow/deposit/withdraw/repay/liduidate actions.
    """

    query_string = f"""
    SELECT 
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index,
        CASE 
            WHEN signature = '{SWAP_IN_SIG}' THEN 'swap_in'
            WHEN signature IN ['{SWAP_OUT_SIG1}','{SWAP_OUT_SIG2}'] THEN 'swap_out'
        END as action
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND signature IN ['{SWAP_IN_SIG}','{SWAP_OUT_SIG1}','{SWAP_OUT_SIG2}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string
