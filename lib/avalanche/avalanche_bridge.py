"""AVALANCHE Bridge Exporter Class"""
import logging
from lib.exporter import Exporter
from lib.avalanche.query import build_events_query
from lib.avalanche.process import process

class AvalancheBridgeExporter(Exporter):
    """
    Avalanche bridge Exporter Class, used to export transactions
    between ethereum and avax-c.
    """
    def __init__(self):
        super().__init__()
        self.name = "avalanche_bridge"

    def read_records(self):
        """
        Read data from clickhouse

        Return: records after clickhouse client execution
        """
        event_query = build_events_query(self.start_dt, self.end_dt)
        event_records = self.read_ch_client.execute(event_query)
        return event_records

    def run(self):
        """The main function to run the Avalanche bridge exporter"""
        self.start_logging()
        records = self.read_records()
        if not records:
            logging.info("No records found for %s", self.name)
            return
        processed_records = process(project_name=self.name, records=records)
        self.insert_records(processed_records)
