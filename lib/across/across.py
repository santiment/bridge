"""Across Exporter Class"""
import logging
from lib.exporter import Exporter
from lib.across.query import build_events_query
from lib.across.process import process

class AcrossExporter(Exporter):
    """
    Across Exporter Class, used to export transactions
    between ethereum and other blockchains.
    """
    def __init__(self):
        super().__init__()
        self.name = "across"

    def read_records(self):
        """
        Read data from clickhouse

        Return: records after clickhouse client execution
        """
        event_query = build_events_query(self.start_dt, self.end_dt)
        event_records = self.read_ch_client.execute(event_query)
        return event_records

    def run(self):
        """The main function to run the Across bridge exporter"""
        self.start_logging()
        records = self.read_records()
        if not records:
            logging.info("No records found for %s", self.name)
            return
        processed_records = process(project_name=self.name, records=records)
        self.insert_records(processed_records)
