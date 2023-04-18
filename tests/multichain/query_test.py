"""Test functions"""
import unittest
from lib.multichain.query import build_events_query
from lib.multichain.process import process
from lib.multichain.multichain import MultichainExporter

# pylint: disable=missing-function-docstring, no-self-use, line-too-long
class TestBuildEventsQuery(unittest.TestCase):
    """Test the build_events query"""
    def test_build_events_query(self):
        start_dt = "2022-01-01 00:00:00"
        end_dt = "2022-01-02 00:00:00"
        query = build_events_query(start_dt, end_dt)
        self.assertIsInstance(query, str)

class TestProcess(unittest.TestCase):
    """Test on process.py"""
    def test_process(self):
        project_name = "multichain"
        records = [
            ("0x123", "0x456",
            '{"amount": "1000", "fromChainID": "1", "toChainID": "2", "token": "0x789", "from": "0xabc", "to": "0xdef"}',
            "2022-01-01 00:00:00", 1, "swap_in", "0x789"),

            ("0x234", "0x567",
            '{"amount": "2000", "fromChainID": "2", "toChainID": "1", "token": "0x890", "from": "0xbcd", "to": "0xef0"}',
            "2022-01-01 00:00:00", 2, "swap_out", "0x890")
        ]
        processed_records = process(project_name, records)
        self.assertIsInstance(next(processed_records), dict)

class TestMultichainExporter(unittest.TestCase):
    """Test class for the exporter"""
    def test_init(self):
        exporter = MultichainExporter()
        self.assertEqual(exporter.name, "multichain")

    def test_read_records(self):
        exporter = MultichainExporter()
        records = exporter.read_records()
        self.assertIsInstance(records, list)

    def test_insert_records(self):
        exporter = MultichainExporter()
        records = [{"dummy": "record"}]
        exporter.dry_run = 1
        exporter.insert_records(records)

    def test_run(self):
        exporter = MultichainExporter()
        exporter.run()

if __name__ == '__main__':
    unittest.main()
