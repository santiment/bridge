"""
Provide utils functions
"""

import logging
import timeit
from functools import wraps


def measure_duration(func):
    """Measure the time duration of a function"""

    @wraps(func)
    def _time_it(*args, **kwargs):
        start = timeit.default_timer()
        try:
            return func(*args, **kwargs)
        finally:
            end_ = timeit.default_timer()
            timing = f"{(end_ - start):.2f} seconds"
            logging.info("Finished in %s", timing)

    return _time_it


def log_iter(iterable, every_size, stop_early=False):
    """Give logging info for iterables"""
    counter = 0
    for item in iterable:
        if stop_early:
            if counter == stop_early:
                break
        if counter == 0:
            logging.info("Processing started")
        counter += 1
        if counter % every_size == 0:
            logging.info("Processed %s trades", counter)

        if item:
            yield item

    logging.info("Processing finished, %s events", counter)

def add_computed_at(events, computed_at):
    """Add computed_at timestamp in event"""
    for event in events:
        event["computed_at"] = computed_at
        yield event
