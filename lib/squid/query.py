"""
Provide functions for clickhouse query in suqid bridge exporter
"""

from lib.constants import ETH_EVENTS_TABLE, ERC20_TRANSFERS_TABLE
from lib.squid.constants import (
    SQUID_ROUTER,
    AXELAR_GATEWAY,
    CONTRACT_CALL_SIG,
)


def build_events_query(start_dt, end_dt):
    """
    Read events from eth_transfers and erc20_transfers table using bridge protoccol contracts
    """

    query_string = f"""
    SELECT
    e.tx_hash as tx_hash,
    any(e.dt) as dt,
    any(contract) as token,
    any(args) as args,
    any(log_index) as log_index,
    any(from) as from
    FROM (
        SELECT
            erc_user.from AS from,
            erc_contract.transactionHash AS transactionHash,
            erc_contract.contract AS contract,
            erc_contract.dt AS dt
        FROM (
            SELECT
                transactionHash,
                contract,
                dt
            FROM
                {ERC20_TRANSFERS_TABLE}
            WHERE
                dt >= toDateTime('{start_dt}')
                AND dt < toDateTime('{end_dt}')
                AND from = '{SQUID_ROUTER}'
                AND to = '{AXELAR_GATEWAY}'
            )
            AS erc_contract
            INNER JOIN (
                SELECT
                from,
                transactionHash,
                contract,
                dt
                FROM
                    {ERC20_TRANSFERS_TABLE}
                WHERE
                    dt >= toDateTime('{start_dt}')
                    AND dt < toDateTime('{end_dt}')
                    AND to = '{SQUID_ROUTER}'
                )
                AS erc_user
            ON erc_user.transactionHash = erc_contract.transactionHash
        )
        AS erc
        INNER JOIN (
        SELECT
            tx_hash,
            contract_addr,
            args,
            dt,
            log_index
        FROM
            {ETH_EVENTS_TABLE}
        WHERE
            dt >= toDateTime('{start_dt}')
            AND dt < toDateTime('{end_dt}')
            AND contract_addr = '{AXELAR_GATEWAY}'
            AND signature = '{CONTRACT_CALL_SIG}'
        ) AS e
        ON erc.transactionHash = e.tx_hash
    GROUP BY tx_hash

    """
    print (query_string)
    return query_string
