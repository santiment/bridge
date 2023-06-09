"""
Provide constants to be used in arbitrum-one exporter
"""

############## ADDRESSES ##############

ARB_BRIDGE = "0x8315177aB297bA92A06054cE80a67Ed4DBd7ed3a".lower()
# deposit eth
ARB_DELAYED_INBOX = "0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f".lower()
ARB_GATEWAY_ROUTER = "0x72Ce9c846789fdB6fC1f34aC4AD25Dd9ef7031ef".lower()
# deposit erc20
ARB_GATEWAY = "0xcEe284F754E854890e311e3280b767F80797180d".lower()
ARB_ERC20_GATEWAY = "0xa3A7B6F88361F48403514059F1F16C8E78d60EeC".lower()

############## SIGNATURES ##############
# withdraw eth
ARB_BRIDGE_CALL_SIG = "0x2d9d115ef3e4a606d698913b1eae831a3cdfe20d9a83d48007b0526749c3d466".lower()
# deposit erc20 sig
ARB_ERC20_DEPOSIT_SIG = "0xb8910b9960c443aac3240b98585384e3a6f109fbf6969e264c3f183d69aba7e1".lower()
# withdraw erc20 sig
ARB_ERC20_WITHDRAW_SIG = "0x891afe029c75c4f8c5855fc3480598bc5a53739344f6ae575bdb7ea2a79f56b3"
ARB_ERC20_WITHDRAW_SIG = ARB_ERC20_WITHDRAW_SIG.lower()

# Deposit eth: user_address -> arb_delayed_inbox -> arb_bridge
#https://github.com/OffchainLabs/nitro/blob/master/contracts/src/bridge/Inbox.sol
