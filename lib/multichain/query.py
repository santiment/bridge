"""
Provide functions for clickhouse query in multichain exporter
"""

from lib.constants import ETH_EVENTS_TABLE
from lib.multichain.constants import (
    SWAP_IN_SIG,
    SWAP_OUT_SIG1,
    SWAP_OUT_SIG2
)
from lib.constants import ERC20_TRANSFERS_TABLE

def build_events_query(start_dt, end_dt):
    """
    Read events from eth_events_v2 table using bridge protoccol contracts
    """

    query_string = f"""
    WITH transfers AS (
        SELECT
            transactionHash,
            contract,
            logIndex
        FROM {ERC20_TRANSFERS_TABLE}
        WHERE
            dt >= toDateTime('{start_dt}')
            AND dt < toDateTime('{end_dt}')
        ORDER BY dt, logIndex
    )
    SELECT 
        tx_hash,
        contract_addr,
        args,
        dt,
        log_index,
        CASE 
            WHEN signature = '{SWAP_IN_SIG}' THEN 'swap_in'
            WHEN signature IN ['{SWAP_OUT_SIG1}','{SWAP_OUT_SIG2}'] THEN 'swap_out'
        END as action,
        CASE 
            WHEN action = 'swap_out' THEN transfers.contract
            WHEN action = 'swap_in' THEN LAST_VALUE(transfers.contract) 
                OVER (PARTITION BY transfers.transactionHash ORDER BY transfers.logIndex)
        END as transfer_contract    
    FROM
        {ETH_EVENTS_TABLE} AS e
        INNER JOIN transfers
        ON e.tx_hash = transfers.transactionHash
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND signature IN ['{SWAP_IN_SIG}','{SWAP_OUT_SIG1}','{SWAP_OUT_SIG2}']
    ORDER BY
        dt DESC,
        log_index DESC
    """
    return query_string
