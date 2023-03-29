"""
The entrance to all exporters
"""

import logging
import fire
from lib.constants import LOG_FORMAT, LOG_LEVEL, LOG_DATE_FORMAT
from lib.wbtc.WBTC import WBTC_Exporter

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt=LOG_DATE_FORMAT)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("clilogger").addHandler(console)


if __name__ == "__main__":
    fire.Fire(
        {
            "wbtc": WBTC_Exporter().run(),
        }
    )
