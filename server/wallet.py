from django.conf import settings
import simplejson as json
from decimal import *
from typing import List
import requests

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])

        return super(DecimalEncoder, self).default(o)

class GridcoinWallet():

    from django.conf import settings

    CONTENT_TYPE = {'content-type': 'application/json'}

    __access_token = None

    def __get_auth_token(self):
        if self.__access_token is not None:
            return self.__access_token

        request_body = {
            "client_id": settings.GRIDCOIN_CLIENT_ID,
            "client_secret": settings.GRIDCOIN_CLIENT_SECRET,
            "audience": settings.GRIDCOIN_AUDIENCE,
            "grant_type":"client_credentials"
        }

        response = requests.post(settings.GRIDCOIN_AUTH_URL, data=json.dumps(request_body), headers=self.CONTENT_TYPE)

        if response.status_code != 200:
            raise
        else:
            content = response.json()

            self.__access_token = content["access_token"]

            return self.__access_token




    def __request_json(url: str, data: Optional[Dict] = None):
        """
        Request JSON data from the GRC full node, given the target command & relevant input parameters.
        More info: http://docs.python-.org/en/master/
        """



        rpc_url="http://"+settings.GRIDCOIN_USER+":"+settings.GRIDCOIN_PASSWORD+"@"+settings.GRIDCOIN_DOMAIN+":"+settings.GRIDCOIN_PORT
        headers = {'content-type': 'application/json'}

        payload = {
                "method": input_method,
                "jsonrpc": "2.0",
                "id": 0
            }

        if (input_parameters != None):
            payload.update({ "params": input_parameters })

        try:
            requested_data = requests.get(rpc_url, data=json.dumps(dict(payload), use_decimal=True), headers=headers)


            if requested_data.status_code != 200:
                return { 'success': False, 'requested_data.status_code':requested_data.status_code, 'response': requested_data.json() }
            else:
                result = requested_data.json()['result']

                return result
        except requests.exceptions.ConnectionError:
            return { 'success': False }

    def get_transaction(self, transaction_id: str):
        return self.__request_json("gettransaction", [transaction_id])

    def list_transactions(self, account="", count=10):
        return self.__request_json("listtransactions", [account, count])

    def get_address(self, account: str):
        return self.__request_json("getaccountaddress", [account])

    def send_payment(self, address: str, amount: Decimal, transaction_id: str):
        return self.__request_json("sendtoaddress", [address, amount, transaction_id])

    def validate_address(self, address: str):
        return self.__request_json("validateaddress", [address])
