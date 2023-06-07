"""
Provide constants to be used in stargate exporter
"""

############## ADDRESSES ##############

ROUTER = "0x8731d54E9D02c286767d56ac03e8037C07e01e98".lower()
ETH_ROUTER = "0x150f94B44927F078737562f0fcF3C95c01Cc2376".lower()

############## SIGNATURES ##############
# swap sig
SWAP_SIG = "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f".lower()
# send credits sig
SEND_CREDITS_SIG = "0x6939f93e3f21cf1362eb17155b740277de5687dae9a83a85909fd71da95944e7".lower()

# Swap: user_address -> Router
# SendCredits: Router -> user_address
# Withdraw not found
