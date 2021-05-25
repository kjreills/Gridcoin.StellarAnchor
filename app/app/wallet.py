import json
from decimal import *
from typing import List
import requests

class GridcoinWallet():

    def __request_json(input_method: str, input_parameters: List):
        """
        Request JSON data from the GRC full node, given the target command & relevant input parameters.
        More info: http://docs.python-.org/en/master/
        """

        from .settings import GRIDCOIN_USER, GRIDCOIN_PASSWORD, GRIDCOIN_DOMAIN, GRIDCOIN_PORT

        rpc_url="http://"+GRIDCOIN_USER+":"+GRIDCOIN_PASSWORD+"@"+GRIDCOIN_DOMAIN+":"+GRIDCOIN_PORT
        headers = {'content-type': 'application/json'}

        payload = {
                "method": input_method,
                "jsonrpc": "2.0",
                "id": 0
            }

        if (input_parameters != None):
            payload.update("params", input_parameters)

        try:
            requested_data = requests.get(rpc_url, data=json.dumps(dict(payload)), headers=headers)

            if requested_data.status_code != 200:
                return { 'success': False, 'requested_data.status_code':requested_data.status_code }
            else:
                result = requested_data.json()['result']

                return result
        except requests.exceptions.ConnectionError:
            return { 'success': False }

    def list_transactions(self, account="", count=10):
        return self.__request_json("listtransactions", [account, count])

    def get_address(self, account: str):
        return self.__request_json("getaccountaddress", [account])

    def send_payment(self, address: str, amount: Decimal, transaction_id: str):
        self.__request_json("sendtoaddress", [address, amount, transaction_id])
