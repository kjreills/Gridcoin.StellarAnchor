from typing import List
from polaris.integrations import RailsIntegration
from polaris.models import Transaction
from django.db.models import QuerySet
from .grcapi import request_json
from logging import getLogger

logger = getLogger("server")

class GrcRailsIntegration(RailsIntegration):
    def poll_pending_deposits(self, pending_deposits: QuerySet) -> List[Transaction]:
        response = request_json("getinfo", None)

        logger.info("**********************************")
        logger.info("getinfo from gridcoin test wallet")
        logger.info(response)
        logger.info("**********************************")

        #return list(pending_deposits)
        return list()

    def execute_outgoing_transaction(self, transaction: Transaction):
        transaction.amount_fee = 0
        transaction.status = Transaction.STATUS.completed
        transaction.save()