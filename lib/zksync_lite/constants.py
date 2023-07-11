"""
Provide constants to be used in zksync_era_bridge exporter
"""

import requests

ZKSYNC_LITE = "0xaBEA9132b05A70803a4E85094fD0e1800777fBEF".lower()
DEPOSIT_SIG = '0x8f5f51448394699ad6a3b80cdadf4ec68c5d724c8c3fea09bea55b3c2d0e2dd0'
WITHDRAWAL_SIG = '0xefef619ae4a542a2b8810b4efeccd8478bd683e985354ee31dd2d644aff6d0ca'

# Get tokens from zksync api
token_dict = {}
TOKEN_API = "https://api.zksync.io/api/v0.1/tokens"
try:
    res = requests.get(TOKEN_API).json()
    token_dict = {x['id']:x['address'] for x in res}
    token_dict[0] = 'ETH'
except requests.exceptions.RequestException as e:
    print(f"Error occurred while making request to TOKEN_API: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
