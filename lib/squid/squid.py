"""Squid Bridge Exporter Class"""
import logging
from lib.exporter import Exporter
from lib.squid.query import build_deposit_query, build_withdraw_query
from lib.squid.process import process

class SquidExporter(Exporter):
    """
    Squid bridge Exporter Class, used to export transactions
    between ethereum and other blockchains.
    """
    def __init__(self):
        super().__init__()
        self.name = "squid"

    def read_records(self):
        """
        Read data from clickhouse

        Return: records after clickhouse client execution
        """
        deposit_query = build_deposit_query(self.start_dt, self.end_dt)
        deposit_records = self.read_ch_client.execute(deposit_query)
        withdraw_query = build_withdraw_query(self.start_dt, self.end_dt)
        withdraw_records = self.read_ch_client.execute(withdraw_query)
        return deposit_records, withdraw_records

    def run(self):
        """The main function to run the squid bridge exporter"""
        self.start_logging()
        deposits, withdraws = self.read_records()
        if not deposits and not withdraws:
            logging.info("No records found for %s", self.name)
            return
        processed_deposit = process(project_name=self.name, records=deposits, action="deposit")
        self.insert_records(processed_deposit)
        processed_withdraw = process(project_name=self.name, records=withdraws, action="withdraw")
        self.insert_records(processed_withdraw)
