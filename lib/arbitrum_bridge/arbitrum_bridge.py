"""Arbitrum bridge Exporter Class"""
import logging
from lib.exporter import Exporter
from lib.arbitrum_bridge.query import (
    build_events_query,
    build_eth_transfer_query
)
from lib.arbitrum_bridge.process import process

class ArbitrumBridgeExporter(Exporter):
    """
    Arbitrum bridge Exporter Class, used to export Arbitrum transactions
    between ethereum and Arbitrum.
    """
    def __init__(self):
        super().__init__()
        self.name = "arbitrum_bridge"

    def read_records(self):
        """
        Read data from clickhouse

        Return: records after clickhouse client execution
        """
        event_query = build_events_query(self.start_dt, self.end_dt)
        eth_transfer_query = build_eth_transfer_query(self.start_dt, self.end_dt)
        event_records = self.read_ch_client.execute(event_query)
        eth_transfer_records = self.read_ch_client.execute(eth_transfer_query)

        return event_records, eth_transfer_records

    def run(self):
        """The main function to run the Arbitrum bridge exporter"""
        self.start_logging()
        event_records, eth_transfer_records = self.read_records()
        if not event_records and not eth_transfer_records:
            logging.info("No records found for %s", self.name)
            return
        processed_event_records = process(project_name=self.name, records=event_records)
        self.insert_records(processed_event_records)

        processed_eth_transfer_records = process(project_name=self.name, records=eth_transfer_records)
        self.insert_records(processed_eth_transfer_records)
