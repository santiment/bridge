"""
Provide constants to be used in squid exporter
"""

############## ADDRESSES ##############

SQUID_ROUTER = "0xce16F69375520ab01377ce7B88f5BA8C48F8D666".lower()
# Deposit: SQUID ROUTER -> Axxxxx Gateway
# Withdraw: Still don't know, could be Axx gateway -> Squid router -> User

############## SIGNATURES ##############
ETH_DEPOSIT_SIG = "0x35d79ab81f2b2017e19afb5c5571778877782d7a8786f5907f93b0f4702f4f23"
ETH_WITHDRAW_SIG = "0x2ac69ee804d9a7a0984249f508dfab7cb2534b465b6ce1580f99a38ba9c5e631"
ERC20_DEPOSIT_SIG = "0x718594027abd4eaed59f95162563e0cc6d0e8d5b86b1c7be8b1b0ac3343d0396"
ERC20_WITHDRAW_SIG = "0x3ceee06c1e37648fcbb6ed52e17b3e1f275a1f8c7b22a84b2b84732431e046b3"
