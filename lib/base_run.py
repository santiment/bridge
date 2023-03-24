"""
Reusable base run function for every exporter
"""

import logging
from datetime import datetime
from clickhouse_driver import Client
from lib.utils import log_iter
from lib.base_queries import insert_query, insert_query_with_args, add_computed_at
from lib.constants import CH_HOST, CH_PORT, START_DT, END_DT, DRY_RUN, READ_CHUNK_SIZE, WRITE_CHUNK_SIZE

logging.getLogger("clilogger")


LOG_FREQUENCY = 100  # every n trades


def base_run(
    name, build_events_query, map_events_to_dictionary, process,
):
    """Reusable base run function for every exporter
        name: name of the project
        build_borrow_query: query function for borrow/deposit/withdraw/repay/liduidate events
        map_events_to_dictionary: mapper from query result to dictionary
        process: mapper from queries results to records for the lending_pools table
    """

    logging.info("Running %s exporter", name)
    logging.info("START_DT=%s", START_DT)
    logging.info("END_DT=%s", END_DT)

    read_ch_client = Client(host=CH_HOST, port=CH_PORT)
    read_settings = {"max_block_size": READ_CHUNK_SIZE}
    write_settings = {"insert_block": WRITE_CHUNK_SIZE}
    write_ch_client = Client(host=CH_HOST, port=CH_PORT, settings=write_settings)

    logging.info("Processing actions...")
    actions_query = build_events_query(START_DT, END_DT)
    records = read_ch_client.execute(actions_query, settings=read_settings)
    if not records:
        logging.info("No records found!")
        return
    events = map_events_to_dictionary(records)
    origin_events = add_computed_at(process(events), datetime.now())
    logged_events = log_iter(origin_events, LOG_FREQUENCY)

    events = map_events_to_dictionary(records)
    events_with_args = add_computed_at(process(events, with_args=True), datetime.now())
    logged_events_with_args = log_iter(events_with_args, LOG_FREQUENCY)

    if DRY_RUN == 1:
        for _ in logged_events_with_args:
            pass
    else:
        # Directly insert records to the lending_pools_events table
        insert = insert_query()
        insert_with_args = insert_query_with_args()
        logging.debug("Insert query: %s", insert)
        logging.debug("Insert query: %s", insert_with_args)
        write_ch_client.execute(insert, logged_events)
        #write_ch_client = Client(host=CH_HOST, port=CH_PORT, settings=write_settings)
        write_ch_client.execute(insert_with_args, logged_events_with_args)
