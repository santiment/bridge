"""
Provide constants to be used in multichain exporter
"""
import json
import os

INFO_PATH = os.path.abspath("lib/multichain/chain_info.json")
############## ADDRESSES ##############

# One of multichain routers
MULTI_ROUTER = "0x7782046601e7b9b05ca55a3899780ce6ee6b8b2b".lower()

############## SIGNATURES ##############

SWAP_IN_SIG = "0xaac9ce45fe3adf5143598c4f18a369591a20a3384aedaf1b525d29127e1fcd55".lower()
SWAP_OUT_SIG1 = "0x409e0ad946b19f77602d6cf11d59e1796ddaa4828159a0b4fb7fa2ff6b161b79".lower()
SWAP_OUT_SIG2 = "0x97116cf6cd4f6412bb47914d6db18da9e16ab2142f543b86e207c24fbd16b23a".lower()

with open(INFO_PATH, encoding="utf-8") as f:
    chain_info = json.load(f)
