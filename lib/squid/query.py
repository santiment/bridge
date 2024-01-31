"""
Provide functions for clickhouse query in suqid bridge exporter
"""

from lib.constants import ETH_EVENTS_TABLE, ERC20_TRANSFERS_TABLE
from lib.squid.constants import (
    SQUID_ROUTER,
    AXELAR_GATEWAY,
    CONTRACT_CALL_SIG,
    WITHDRAW_SIG
)

def build_withdraw_query(start_dt, end_dt):
    """
    Query that get records for tokens transfered from other chains to ethereum
    """
    query_string = f"""
    SELECT
        tx_hash,
        dt,
        args,
        log_index,
        '{SQUID_ROUTER}' AS user
    FROM
        {ETH_EVENTS_TABLE}
    WHERE
        dt >= toDateTime('{start_dt}')
        AND dt < toDateTime('{end_dt}')
        AND contract_addr = '{AXELAR_GATEWAY}'
        AND signature = '{WITHDRAW_SIG}'
    """
    return query_string


def build_deposit_query(start_dt, end_dt):
    """
    Read events from eth_transfers and erc20_transfers table using bridge protoccol contracts
    """

    query_string = f"""
    SELECT
    e.tx_hash AS tx_hash,
    any(e.dt) AS dt,
    any(contract) AS token,
    any(args) AS args,
    any(log_index) AS log_index,
    any(from) AS from
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
    return query_string
