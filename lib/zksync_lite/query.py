"""
Provide functions for clickhouse query in zksync_lite exporter
"""

from lib.constants import ETH_EVENTS_TABLE, ETH_TRANSFERS_TABLE
from lib.zksync_lite.constants import (
    ZKSYNC_LITE,
    ZKSYNC_DIAMOND_PROXY,
    DEPOSIT_INITIATED_SIG,
    WITHDRAWAL_FINALIZED_SIG,
    ETH_WITHDRAWAL_FINALIZED_SIG
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_events_v2 table using zksync_lite contracts
    """

    query_string = f"""
    SELECT 
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index,
        CASE
            WHEN signature = '{DEPOSIT_INITIATED_SIG}' THEN 'deposit'  # This will now include the new deposit event
            WHEN signature = '{WITHDRAWAL_FINALIZED_SIG}' THEN 'withdraw'
            WHEN signature = '{ETH_WITHDRAWAL_FINALIZED_SIG}' THEN 'eth_withdraw'
        END as action
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr IN ['{ZKSYNC_LITE}', '{ZKSYNC_DIAMOND_PROXY}']
        AND signature IN ['{DEPOSIT_INITIATED_SIG}', '{WITHDRAWAL_FINALIZED_SIG}', '{ETH_WITHDRAWAL_FINALIZED_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string


def build_transfers_query(start_dt, end_dt):
    """
    Using eth_transfers to determine the ETH flow for zksync_lite
    """
    query_string = f"""
    SELECT
        transactionHash,
        dt,
        from,
        value,
        'eth_deposit' as action
    FROM {ETH_TRANSFERS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND to = '{ZKSYNC_DIAMOND_PROXY}'
        AND from != '{ZKSYNC_LITE}'
    """
    return query_string
