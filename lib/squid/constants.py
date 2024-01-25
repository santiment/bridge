"""
Provide constants to be used in squid exporter
"""

############## ADDRESSES ##############

SQUID_ROUTER = "0xce16F69375520ab01377ce7B88f5BA8C48F8D666".lower()
AXELAR_GATEWAY = "0x4F4495243837681061C4743b74B3eEdf548D56A5".lower()
# Deposit: SQUID ROUTER -> Axxxxx Gateway
# Withdraw: Still don't know, could be Axx gateway -> Squid router -> User

############## SIGNATURES ##############
CONTRACT_CALL_SIG = "0x7e50569d26be643bda7757722291ec66b1be66d8283474ae3fab5a98f878a7a2"
WITHDRAW_SIG = "0x9991faa1f435675159ffae64b66d7ecfdb55c29755869a18db8497b4392347e0"