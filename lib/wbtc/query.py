"""
Provide functions for clickhouse query in wbtc exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.wbtc.constants import (
    WBTC_FACTORY,
    MINT_CONFIRMED_SIG,
    BURNED_CONFIRMED_SIG
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
            WHEN signature = '{MINT_CONFIRMED_SIG}' THEN 'mint'
            WHEN signature = '{BURNED_CONFIRMED_SIG}' THEN 'burn'
        END as action
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{WBTC_FACTORY}'
        AND signature = '{MINT_CONFIRMED_SIG}'
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string
