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

    @staticmethod
    def __request_json(input_method: str, input_parameters: List):
        """
        Request JSON data from the GRC full node, given the target command & relevant input parameters.
        More info: http://docs.python-.org/en/master/
        """

        from .settings import GRIDCOIN_USER, GRIDCOIN_PASSWORD, GRIDCOIN_DOMAIN, GRIDCOIN_PORT

        # GRIDCOIN_USER="rpcuser"
        # GRIDCOIN_PASSWORD="@sdsdfj9252kdsk"
        # GRIDCOIN_DOMAIN="192.168.1.100"
        # GRIDCOIN_PORT="9000"

        rpc_url="http://"+GRIDCOIN_USER+":"+GRIDCOIN_PASSWORD+"@"+GRIDCOIN_DOMAIN+":"+GRIDCOIN_PORT
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
