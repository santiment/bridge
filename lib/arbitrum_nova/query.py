"""
Provide functions for clickhouse query in arbitrum bridge exporter
"""

from lib.constants import ETH_EVENTS_TABLE, ETH_TRANSFERS_TABLE
from lib.arbitrum_nova.constants import (
    ARB_BRIDGE,
    ARB_GATEWAY,
    ARB_ERC20_GATEWAY,
    ARB_DELAYED_INBOX,
    ARB_BRIDGE_CALL_SIG,
    ARB_ERC20_DEPOSIT_SIG,
    ARB_ERC20_WITHDRAW_SIG,
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
            WHEN signature IN ['{ARB_BRIDGE_CALL_SIG}', '{ARB_ERC20_WITHDRAW_SIG}'] THEN 'withdraw'
            WHEN signature IN ['{ARB_ERC20_DEPOSIT_SIG}'] THEN 'deposit'
        END as action,
        CASE 
            WHEN signature = '{ARB_BRIDGE_CALL_SIG}' THEN 'eth'
            ELSE 'erc20'
        END as token_type
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr IN ['{ARB_BRIDGE}', '{ARB_GATEWAY}', '{ARB_ERC20_GATEWAY}']
        AND signature IN ['{ARB_BRIDGE_CALL_SIG}', '{ARB_ERC20_DEPOSIT_SIG}', '{ARB_ERC20_WITHDRAW_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string

def build_eth_deposit_query(start_dt, end_dt):
    """
    Build query for arb bridge eth deposits.
    Deposit eth route: user_address -> arb_delayed_inbox -> arb_bridge
    """
    query_string = f"""
    SELECT 
        transactionHash,
        dt,
        from,
        value
    FROM {ETH_TRANSFERS_TABLE}
    WHERE 
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND to = '{ARB_DELAYED_INBOX}'
        AND from NOT IN ['{ARB_BRIDGE}', '{ARB_GATEWAY}', '{ARB_ERC20_GATEWAY}']
    """

    return query_string
