"""
Provide functions for clickhouse query in stargate exporter
"""

from lib.constants import ETH_EVENTS_TABLE


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
        END as action,
        CASE 
            WHEN signature = '{SWAP_SIG}' THEN 'eth'
            ELSE 'erc20'
        END as token_type
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr IN ['{Router}', '{ETH_Router}']
        AND signature IN ['{SWAP_SIG}', '{SEND_CREDITS_SIG}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string

