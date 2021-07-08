from django.conf import settings
from requests.api import head
import simplejson as json
from decimal import *
from typing import List, Optional, Dict
import requests
from logging import getLogger

logger = getLogger("server")

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

            logger.info(self.__access_token)

            return self.__access_token

    def __request_json(self, url: str, data: Dict = {}):
        """
        Request JSON data from the GRC full node, given the target command & relevant input parameters.
        """
        try:
            headers = self.CONTENT_TYPE.copy()
            headers.update({ "Authorization": "Bearer " + self.__get_auth_token() })

            response = requests.get(f"{settings.GRIDCOIN_API_URL}/Gridcoin/{url}", data=json.dumps(dict(data), use_decimal=True), headers=headers)

            if response.status_code != 200:
                logger.warn(f"Non-200 status code returned for request to {url}. Response: {response.text}. Status code: {response.status_code}")

                return { 'success': False, 'status_code':response.status_code, 'response': response }
            else:
                result = response.json()['result']

                return result
        except requests.exceptions.ConnectionError as ex:
            logger.error("Connection Error occurred", exc_info=ex)

            return { 'success': False }

    def get_transaction(self, transaction_id: str):
        return self.__request_json(f"getTransaction/{transaction_id}")

    def list_transactions(self, account="", count=10):
        return self.__request_json(f"listTransactions?account={account}&count={count}")

    def get_address(self, account: str):
        return self.__request_json(f"getAccountAddress/{account}")

    def send_payment(self, address: str, amount: Decimal, transaction_id: str):
        payload = {
            address: address,
            amount: amount,
            "transactionId": transaction_id
        }

        return self.__request_json(f"sendToAddress", payload)

    def validate_address(self, address: str):
        return self.__request_json(f"validateAddress/{address}")
