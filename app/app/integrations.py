from typing import List, Optional, Dict
from base64 import b64encode
from typing_extensions import get_type_hints
from polaris.integrations import RailsIntegration, DepositIntegration
from polaris.models import Transaction
from polaris.templates import Template
from django.db.models import QuerySet
from django import forms
from .grcapi import listTransactions, getTransaction, getAddress
from logging import getLogger

logger = getLogger("server")

class GrcDepositIntegration(DepositIntegration):
    # def process_sep6_request(self, params, transaction: Transaction):
    #     if transaction.asset.code is not "GRC":
    #         return {
    #             "error": "This anchor doesn't support the given currency code: ETH"
    #         }

    #     #Create GRC address with label=transaction id
    #     #return address to send funds to

    #     return {

    #     }

    def content_for_template(
        self,
        template: Template,
        form: Optional[forms.Form] = None,
        transaction: Optional[Transaction] = None,
    ) -> Optional[Dict]:
        #na, kyc_content = SEP24KYC.check_kyc(transaction)
        #if kyc_content:
        #    return kyc_content
        if template == Template.DEPOSIT:
            if not form:
                return None

            return {
                "title": "Polaris Transaction Information",
                "guidance": "Please enter the amount you would like to transfer.",
                "icon_label": "Gridcoin Anchor",
            }
        elif template == Template.MORE_INFO:
            content = {
                "title": "Polaris Transaction Information",
                "icon_label": "Gridcoin Anchor",
            }
            if transaction.status == Transaction.STATUS.pending_user_transfer_start:
                # We're waiting on the user to send an off-chain payment
                offChainAddress = getAddress(str(transaction.id))
                content.update(
                    memo=b64encode(str(hash(transaction)).encode())
                    .decode()[:10]
                    .upper(),
                    instructions="To complete your deposit, send the correct amount of GRC from your Gridcoin wallet to address: {a}".format(a=offChainAddress)
                )
            return content



class GrcRailsIntegration(RailsIntegration):
    CONSTANT_FEE_GRC = 0.1

    def __received(self, grc_transaction: Dict):
        return grc_transaction.get("category") == "receive"

    def __amount(self, grc_transaction: Dict):
        return grc_transaction.get("amount")

    def poll_pending_deposits(self, pending_deposits: QuerySet) -> List[Transaction]:

        ready_deposits = []

        for deposit in pending_deposits:
            print("Deposit pending: {}".format(str(deposit.id)))
            grc_transactions = listTransactions(str(deposit.id))

            if (grc_transactions == []):
                continue

            grc_deposits = filter (self.__received, grc_transactions)
            total_deposited = sum(map(self.__amount, grc_deposits))

            deposit.amount_in = total_deposited
            deposit.amount_fee = self.CONSTANT_FEE_GRC
            deposit.save()
            ready_deposits.append(deposit)

        return ready_deposits

        # logger.info("**********************************")
        # logger.info("getinfo from gridcoin test wallet")
        # logger.info(transactions)
        # logger.info("**********************************")

        # #return list(pending_deposits)
        # return list()

    def execute_outgoing_transaction(self, transaction: Transaction):
        transaction.amount_fee = 0
        transaction.status = Transaction.STATUS.completed
        transaction.save()