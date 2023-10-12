"""
The entrance to all exporters
"""

import logging
import fire
from lib.constants import LOG_FORMAT, LOG_LEVEL, LOG_DATE_FORMAT
from lib.wbtc.wbtc import WBTCExporter
from lib.multichain.multichain import MultichainExporter
from lib.arbitrum_one.arbitrum_one import ArbitrumOneExporter
from lib.arbitrum_nova.arbitrum_nova import ArbitrumNovaExporter
from lib.polygon_bridge.polygon_bridge import PolygonBridgeExporter
from lib.stargate.stargate import StargateExporter
from lib.zksync_era_bridge.zksync_era_bridge import ZksyncEraBridgeExporter
from lib.zksync_lite.zksync_lite import ZksyncLiteExporter

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, datefmt=LOG_DATE_FORMAT)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("clilogger").addHandler(console)


if __name__ == "__main__":
    fire.Fire(
        {
            "wbtc": WBTCExporter().run,
            "multichain": MultichainExporter().run,
            "arbitrum_one": ArbitrumOneExporter().run,
            "arbitrum_nova": ArbitrumNovaExporter().run,
            "polygon_bridge": PolygonBridgeExporter().run,
            "stargate": StargateExporter().run,
            "zksync_era_bridge": ZksyncEraBridgeExporter().run,
            "zksync_lite": ZksyncLiteExporter().run
        }
    )
