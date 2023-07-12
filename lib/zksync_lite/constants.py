"""
Provide constants to be used in zksync_era_bridge exporter
"""

import logging
import requests
from retry import retry
from requests.exceptions import RequestException, Timeout, HTTPError


ZKSYNC_LITE = "0xaBEA9132b05A70803a4E85094fD0e1800777fBEF".lower()
DEPOSIT_SIG = '0x8f5f51448394699ad6a3b80cdadf4ec68c5d724c8c3fea09bea55b3c2d0e2dd0'
WITHDRAWAL_SIG = '0xefef619ae4a542a2b8810b4efeccd8478bd683e985354ee31dd2d644aff6d0ca'


TOKEN_API = "https://api.zksync.io/api/v0.1/tokens"

@retry(requests.exceptions.RequestException, tries=3, delay=2, backoff=2)
def get_token_dict():
    """Get token id info from zksync api"""
    res = requests.get(TOKEN_API, timeout=5).json()
    token_address_id = {x['id']:x['address'] for x in res}
    token_address_id[0] = 'ETH'
    return token_address_id

try:
    TOKEN_DICT = get_token_dict()
except Timeout as timeout_exception:
    logging.info("Request timed out: %s", timeout_exception)
    TOKEN_DICT = None
except HTTPError as http_error:
    logging.info("HTTP error occurred: %s", http_error)
    TOKEN_DICT = None
except ConnectionError as connection_error:
    print("Connection error occurred:", connection_error)
    TOKEN_DICT = None
except RequestException as request_exception:
    logging.info("Error occurred while making request to TOKEN_API: %s", request_exception)
    TOKEN_DICT = None
