"""
Provide constants to be used in Across exporter
"""

import json
import os

############## ADDRESSES ##############

ACROSS_BRIDGE = "0x5c7bcd6e7de5423a257d81b442095a1a6ced35c5".lower()
ACROSS_POOL = "0xc186fa914353c44b2e33ebe05f21846f1048beda".lower()

############## SIGNATURES ##############

FUNDS_DEPOSIT_SIG = "0xafc4df6845a4ab948b492800d3d8a25d538a102a2bc07cd01f1cfa097fddcff6"
FILLED_RELAY_SIG = "0x8ab9dc6c19fe88e69bc70221b339c84332752fdd49591b7c51e66bae3947b73c"

############## CHAIN ID ##############
ID_PATH = os.path.abspath("lib/across/chain_id.json")
with open(ID_PATH, encoding="utf-8") as f:
    chain_id = json.load(f)
