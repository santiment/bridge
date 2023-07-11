"""
Provide functions for clickhouse query in zksync_lite exporter
"""

from lib.constants import ETH_EVENTS_TABLE, ETH_RECEIPTS_TABLE
from lib.zksync_lite.constants import (
    ZKSYNC_LITE,
    DEPOSIT_SIG,
    WITHDRAWAL_SIG
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
            WHEN signature = '{DEPOSIT_SIG}' THEN 'deposit' 
            WHEN signature = '{WITHDRAWAL_SIG}' THEN 'withdraw'
        END as action,
        r.from
    FROM
        {ETH_EVENTS_TABLE} AS e
    INNER JOIN
        (SELECT
            from,
            transactionHash
        FROM {ETH_RECEIPTS_TABLE}
        WHERE 
            dt >= toDateTime('{start_dt}')
            AND dt < toDateTime('{end_dt}')
        ) AS r
    ON r.transactionHash = e.tx_hash
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{ZKSYNC_LITE}'
        AND signature IN ['{DEPOSIT_SIG}', '{WITHDRAWAL_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string
