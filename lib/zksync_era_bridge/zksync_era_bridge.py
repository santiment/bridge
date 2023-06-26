"""Zksync era bridge Exporter Class"""
import logging
from lib.exporter import Exporter
from lib.zksync_era_bridge.query import build_events_query
from lib.zksync_era_bridge.process import process

class ZksyncEraBridgeExporter(Exporter):
    """
    Zksync era bridge Exporter Class, used to export transactions
    between ethereum and zksync.
    """
    def __init__(self):
        super().__init__()
        self.name = "zksync_era_bridge"

    def read_records(self):
        """
        Read data from clickhouse

        Return: records after clickhouse client execution
        """
        read_query = build_events_query(self.start_dt, self.end_dt)
        records = self.read_ch_client.execute(read_query)

        return records

    def run(self):
        """The main function to run the zksync era bridge exporter"""
        self.start_logging()
        records = self.read_records()
        if not records:
            logging.info("No records found for %s", self.name)
            return
        processed_records = process(project_name=self.name, records=records)
        self.insert_records(processed_records)
