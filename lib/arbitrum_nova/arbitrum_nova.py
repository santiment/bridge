"""Arbitrum-nova bridge Exporter Class"""
import logging
from lib.exporter import Exporter
from lib.arbitrum_nova.query import (
    build_events_query,
    build_eth_deposit_query
)
from lib.arbitrum_nova.process import process

class ArbitrumNovaExporter(Exporter):
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
        eth_transfer_query = build_eth_deposit_query(self.start_dt, self.end_dt)
        event_records = self.read_ch_client.execute(event_query)
        eth_transfer_records = self.read_ch_client.execute(eth_transfer_query)
        event_records.extend(eth_transfer_records)
        return event_records

    def run(self):
        """The main function to run the Arbitrum bridge exporter"""
        self.start_logging()
        records = self.read_records()
        if not records:
            logging.info("No records found for %s", self.name)
            return
        processed_event_records = process(
            project_name=self.name,
            records=records
        )
        self.insert_records(processed_event_records)
