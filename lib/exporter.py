"""
The Exporter class, providing general settings and interface for every exporter
"""
import logging
from clickhouse_driver import Client
from lib.constants import (
    CH_HOST, CH_PORT,
    START_DT, END_DT,
    DRY_RUN, READ_CHUNK_SIZE,
    WRITE_CHUNK_SIZE,
    BRIDGE_TRANSACTIONS_TABLE
)

class Exporter:
    """
    The exporter class, every exporter should implement its own functions:
    read_records, insert_records and run.
    """
    # pylint: disable=unnecessary-pass
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
        """Read data from clickhouse"""
        pass

    def run(self):
        """The main function to run the exporter"""
        pass

    def insert_records(self, records):
        """
        Write the processed data to clickhouse

        param:
            records: Processed records generator from process function
        """
        logging.debug("Insert query: %s", self.insert_query)
        if self.dry_run != 1:
            self.write_ch_client.execute(self.insert_query, records)
            return
        # If dry run mode, do nothing
        for record in records:
            print (record)

    def start_logging(self):
        """Start logging in the exporter"""
        logging.getLogger("clilogger")
        logging.info("Running %s exporter", self.name)
        logging.info("START_DT=%s", self.start_dt)
        logging.info("END_DT=%s", self.end_dt)
