from django.conf import settings
import simplejson as json
from decimal import *
from typing import Any, Dict
import requests
from logging import exception, getLogger
from result import Ok, Err, Result

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

            return self.__access_token

    def __request(self, method, url, data: Dict = {}) -> Result[Any,Exception]:
        try:
            headers = self.CONTENT_TYPE.copy()
            headers.update({ "Authorization": "Bearer " + self.__get_auth_token() })

            response = requests.request(method, f"{settings.GRIDCOIN_API_URL}/Gridcoin/{url}", headers=headers, data=json.dumps(data, cls=DecimalEncoder))

            if response.status_code != 200:
                logger.warn(f"Non-200 status code returned for request to {url}. Response: {response.text}. Status code: {response.status_code}")

                return Err(exception("Non-200 status code returned from the server", { response.status_code }))
            else:
                result = response.json()['result']

                return Ok(result)
        except requests.exceptions.ConnectionError as ex:
            logger.error("Connection error occurred", exc_info=ex)

            return Err(ex)

    def __get(self, url: str):
        return self.__request("GET", url)

    def __post(self, url: str, data: Dict = {}):
        return self.__request("POST", url, data)

    def get_transaction(self, transaction_id: str):
        logger.info(f"get_transaction: {transaction_id}")

        return self.__get(f"getTransaction/{transaction_id}")

    def list_transactions(self, account="", count=10):
        logger.info(f"list_transactions: {account}")

        return self.__get(f"listTransactions?account={account}&count={count}")

    def get_address(self, account: str):
        logger.info(f"get_address: {account}")

        return self.__get(f"getAccountAddress/{account}")

    def send_payment(self, address: str, amount: Decimal, transaction_id: str):
        payload = {
            "address": address,
            "amount": amount,
            "transactionId": transaction_id
        }

        logger.info(f"send_payment: {payload}")

        return self.__post(f"sendToAddress", payload)

    def validate_address(self, address: str):
        logger.info(f"send_payment: {address}")

        return self.__get(f"validateAddress/{address}")
