"""Multichain exporter class"""
import logging
from lib.exporter import Exporter
from lib.multichain.query import build_events_query
from lib.multichain.process import process

class MultichainExporter(Exporter):
    """
    Multichain Exporter Class, used to export transactions
    between multiple blockchains in a Multichain network.
    """
    def __init__(self):
        super().__init__()
        self.name = "multichain"

    def read_records(self):
        """
        Read data from Multichain node

        Return: records after executing the query on the Multichain node
        """
        read_query = build_events_query(self.start_dt, self.end_dt)
        records = self.read_ch_client.execute(read_query)

        return records

    def run(self):
        """The main function to run the Multichain exporter"""
        self.start_logging()
        records = self.read_records()
        if not records:
            logging.info("No records found for %s", self.name)
            return
        processed_records = process(project_name=self.name, records=records)
        self.insert_records(processed_records)
