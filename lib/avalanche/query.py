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
        FROM (
            SELECT DISTINCT
                dt,
                transactionHash,
                from,
                to,
                value,
                contract
            FROM {ERC20_TRANSFERS_TABLE}
            WHERE to = '{ETH_AVAX_BRIDGE}'
            AND dt > toDateTime('{start_dt}')
            AND dt < toDateTime('{end_dt}')

        ) INNER JOIN (
            SELECT avax_tx_hash, concat('0x', substr(args, 259, 64)) as transactionHash FROM (

                SELECT DISTINCT transactionHash as avax_tx_hash, topics, args
                FROM {AVAX_RECEIPTS_TABLE}

                ARRAY JOIN
                    logs.topics as topics,
                    logs.data as args

                WHERE dt > toDateTime('{start_dt}')
                AND dt < toDateTime('{end_dt}')
            )
            WHERE topics[1] = '{ETH_AVAX_TRANSFER_SIG}'
        ) USING transactionHash
        ORDER BY dt)

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
            AND dt > toDateTime('{start_dt}')
            AND dt < toDateTime('{end_dt}')
        ORDER BY dt
        )
    '''
    return query
