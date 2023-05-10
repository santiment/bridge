"""
Provide constants to be used in arbitrum-nova exporter
"""

############## ADDRESSES ##############

ARB_BRIDGE = "0xC1Ebd02f738644983b6C4B2d440b8e77DdE276Bd".lower()
# deposit eth
ARB_DELAYED_INBOX = "0xc4448b71118c9071Bcb9734A0EAc55D18A153949".lower()
# deposit erc20
ARB_GATEWAY = "0x23122da8C581AA7E0d07A36Ff1f16F799650232f".lower()
ARB_ERC20_GATEWAY = "0xB2535b988dcE19f9D71dfB22dB6da744aCac21bf".lower()

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
