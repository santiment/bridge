"""
Provide constants to be used in stargate exporter
"""
import lib.constants as const

############## ADDRESSES ##############

ROUTER = "0x8731d54E9D02c286767d56ac03e8037C07e01e98".lower()
ETH_ROUTER = "0x150f94B44927F078737562f0fcF3C95c01Cc2376".lower()

############## SIGNATURES ##############
# deposit sig
SWAP_SIG = "0x34660fc8af304464529f48a778e03d03e4d34bcd5f9b6f0cfbf3cd238c642f7f".lower()
# withdraw sigs
SWAP_REMOTE_SIG = "0xfb2b592367452f1c437675bed47f5e1e6c25188c17d7ba01a12eb030bc41ccef".lower()
CREDIT_CHAIN_PATH_SIG = "0xdbdd25248751feb2f3b66721dfdd11662a68bc155af3771e661aabec92fba814".lower()

############## Chain ID ################
# Reference: https://stargateprotocol.gitbook.io/stargate/developers/chain-ids
CHAIN_DICT = {
    "101": const.ETHEREUM,
    "102": const.BSC,
    "106": const.AVALANCHE,
    "109": const.POLYGON,
    "110": const.ARBITRUM_NOVA,
    "111": const.AVALANCHE,
    "112": const.FANTOM,
    "151": const.METIS
}
# Swap: user_address -> Router
# SendCredits: Router -> user_address
# Withdraw not found
