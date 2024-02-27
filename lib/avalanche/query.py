"""
Provide functions for clickhouse query in avalanche bridge exporter
"""

from lib.constants import ERC20_TRANSFERS_TABLE, AVAX_RECEIPTS_TABLE
from lib.avalanche.constants import (
    ETH_AVAX_BRIDGE,
    ETH_AVAX_TRANSFER_SIG
)


def build_events_query(start_dt, end_dt):
    """
    Read events from erc20_transfers and avax_reciepts table using avalanche protoccol addresses
    """

    query = f'''
        (SELECT
            dt,
            transactionHash,
            from,
            to,
            value,
            contract,
            'deposit' as action
        FROM {ERC20_TRANSFERS_TABLE}
        WHERE to = '{ETH_AVAX_BRIDGE}'
        AND dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        ORDER BY dt
        )

        UNION ALL

        (
        SELECT
            dt,
            transactionHash,
            from,
            to,
            value,
            contract,
            'withdraw' as action
        FROM {ERC20_TRANSFERS_TABLE}
        WHERE from = '{ETH_AVAX_BRIDGE}'
        AND dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        ORDER BY dt
        )
    '''
    return query
