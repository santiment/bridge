"""
Provide functions for clickhouse query in op_bridge exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.manta_pacific.constants import (
    MANTA_PACIFIC_BRIDGE,
    ETH_DEPOSIT_SIG,
    ETH_WITHDRAW_SIG,
    ERC20_DEPOSIT_SIG,
    ERC20_WITHDRAW_SIG
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
        CASE 
            WHEN signature IN ['{ETH_DEPOSIT_SIG}', '{ETH_WITHDRAW_SIG}'] THEN 'eth'
            ELSE 'erc20'
        END as token_type,
        CASE
            WHEN signature IN ['{ETH_DEPOSIT_SIG}', '{ERC20_DEPOSIT_SIG}'] THEN 'deposit'
            ELSE 'withdraw'
        END as action

    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{MANTA_PACIFIC_BRIDGE}'
        AND signature IN [
            '{ETH_DEPOSIT_SIG}',
            '{ETH_WITHDRAW_SIG}',
            '{ERC20_DEPOSIT_SIG}',
            '{ERC20_WITHDRAW_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string
