"""
The Exporter class, providing general settings and interface for every exporter
"""
from clickhouse_driver import Client
from lib.constants import (
    CH_HOST, CH_PORT,
    START_DT, END_DT,
    DRY_RUN, READ_CHUNK_SIZE,
    WRITE_CHUNK_SIZE,
    BRIDGE_TRANSACTIONS_TABLE
)

class Exporter:
    def __init__(self):
        read_settings = {"max_block_size": READ_CHUNK_SIZE}
        write_settings = {"insert_block": WRITE_CHUNK_SIZE}
        self.read_ch_client = Client(host=CH_HOST, port=CH_PORT, settings=read_settings)
        self.write_ch_client = Client(host=CH_HOST, port=CH_PORT, settings=write_settings)
        self.start_dt, self.end_dt = START_DT, END_DT
        self.dry_run = DRY_RUN
        self.insert_query = f"""
            INSERT INTO {BRIDGE_TRANSACTIONS_TABLE}
                (tx_hash, log_index, dt, chain_in, chain_out, contract_addr, token_in, 
                token_out, amount_in, amount_out, project_name, user, args, computed_at)
            VALUES
        """

        self.name = None

    def read_records(self):
        pass

    def run(self):
        pass

    def process(self):
        pass

    def insert_records(self):
        pass
