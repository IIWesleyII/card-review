# https://developers.coinbase.com/api/v2
# https://developers.coinbase.com/docs/wallet/api-key-authentication
# https://medium.com/@samhagin/check-your-balance-on-coinbase-using-python-5641ff769f91

import hmac, hashlib, time, requests, os, codecs
from requests.auth import AuthBase
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

# Create custom authentication for Coinbase API
class CoinbaseWalletAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or '')
        signature = hmac.new(codecs.encode(self.secret_key), codecs.encode(message), hashlib.sha256).hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
        })
        return request

api_url = "https://api.coinbase.com/v2/"
auth = CoinbaseWalletAuth(API_KEY, API_SECRET)



# GET current user
r = requests.get(api_url + "user", auth=auth)
print(r.json())

