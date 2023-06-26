"""
Provide functions for clickhouse query in zksync_era_bridge exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.zksync_era_bridge.constants import (
    ZKSYNC_ERA_BRIDGE,
    DEPOSIT_INITIATED_SIG
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_events_v2 table using zksync_era_bridge contracts
    """

    query_string = f"""
    SELECT 
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index,
        CASE
            WHEN signature = '{DEPOSIT_INITIATED_SIG}' THEN 'deposit_initiated'
        END as action
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{ZKSYNC_ERA_BRIDGE}'
        AND signature IN ['{DEPOSIT_INITIATED_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string
