"""
Provide functions for clickhouse query in stargate exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.stargate.constants import (
    SWAP_SIG,
    CREDIT_CHAIN_PATH_SIG,
    SWAP_REMOTE_SIG
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_events_v2 table using stargate contracts
    """

    query_string = f"""
    WITH chain_path AS (
    SELECT
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index
    FROM {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND signature = '{CREDIT_CHAIN_PATH_SIG}'
    )

    SELECT 
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index,
        CASE 
            WHEN e.signature = '{SWAP_SIG}' THEN 'deposit'
            WHEN e.signature = '{SWAP_REMOTE_SIG}' THEN 'withdraw'
        END as action,
        chain_path.args as chain_args     
    FROM
        {ETH_EVENTS_TABLE} AS e 
        LEFT JOIN chain_path
        ON e.tx_hash = chain_path.tx_hash
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND e.signature IN ['{SWAP_SIG}', '{SWAP_REMOTE_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string
