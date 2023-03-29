"""WBTC Exporter Class"""
import logging
from lib.Exporter import Exporter
from lib.wbtc.query import build_events_query
from lib.wbtc.process import process

class WBTC_Exporter(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "wbtc"

    def read_records(self):
        """Read data from clickhouse"""
        read_query = build_events_query(self.start_dt, self.end_dt)
        records = self.read_ch_client.execute(read_query)
        
        return records

    def insert_records(self, records):
        """Write the processed data to clickhouse"""
        logging.debug("Insert query: %s", self.insert_query)
        if self.dry_run != 1:
            self.write_ch_client.execute(self.insert_query, records)
            return
        # If dry run mode, do nothing
        for r in records:
            print (r)

    def start_logging(self):
        logging.getLogger("clilogger")
        logging.info("Running %s exporter", self.name)
        logging.info("START_DT=%s", self.start_dt)
        logging.info("END_DT=%s", self.end_dt)
        
    def run(self):
        """The main function to run the WBTC exporter"""
        self.start_logging()
        records = self.read_records()
        if not records:
            logging.info("No records found!")
            return
        processed_records = process(project_name=self.name, records=records)
        self.insert_records(processed_records)