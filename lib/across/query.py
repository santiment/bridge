"""
Provide functions for clickhouse query in across bridge exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.across.constants import (
    ACROSS_BRIDGE,
    FUNDS_DEPOSIT_SIG,
    FILLED_RELAY_SIG
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_transfers and erc20_transfers table using bridge protoccol contracts
    """

    query_string = f"""
    SELECT 
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index,
        signature
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{ACROSS_BRIDGE}'
        AND signature IN ['{FUNDS_DEPOSIT_SIG}', '{FILLED_RELAY_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string
