from typing import List, Optional, Dict
from decimal import *
from base64 import b64encode
from typing_extensions import get_type_hints
from polaris.integrations import RailsIntegration, DepositIntegration
from polaris.models import Transaction
from polaris.templates import Template
from polaris import settings
from django.db.models import QuerySet
from django import forms
from .wallet import GridcoinWallet
from logging import getLogger

logger = getLogger("server")

class Utility:
    def calculate_fee(fee_params: Dict) -> Decimal:
        DEPOSIT_FEE = Decimal('0')
        WITHDRAWAL_FEE = Decimal('0.001') * fee_params["amount"] # 0.1% withdrawal fee

        if fee_params["operation"] == settings.OPERATION_WITHDRAWAL:
            return WITHDRAWAL_FEE
        else:
            return DEPOSIT_FEE


class GrcDepositIntegration(DepositIntegration):
    __wallet = GridcoinWallet()

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
                offChainAddress = self.__wallet.get_address(str(transaction.id))
                content.update(
                    memo=b64encode(str(hash(transaction)).encode())
                    .decode()[:10]
                    .upper(),
                    instructions="To complete your deposit, send the correct amount of GRC from your Gridcoin wallet to address: {a}".format(a=offChainAddress)
                )
            return content



class GrcRailsIntegration(RailsIntegration):
    __wallet = GridcoinWallet()

    def __received(self, grc_transaction: Dict):
        return grc_transaction.get("category") == "receive"

    def __amount(self, grc_transaction: Dict):
        return grc_transaction.get("amount")

    def poll_pending_deposits(self, pending_deposits: QuerySet) -> List[Transaction]:

        ready_deposits = []

        for deposit in pending_deposits:
            grc_transactions = self.__wallet.list_transactions(str(deposit.id))

            if (grc_transactions == []):
                continue

            grc_deposits = filter (self.__received, grc_transactions)
            total_deposited = sum(map(self.__amount, grc_deposits))

            deposit.amount_in = total_deposited
            deposit.amount_fee = Utility.calculate_fee({
                        "amount": deposit.amount_in,
                        "operation": settings.OPERATION_DEPOSIT,
                        "asset_code": deposit.asset.code,
                    })
            deposit.save()
            ready_deposits.append(deposit)

        return ready_deposits

    def execute_outgoing_transaction(self, transaction: Transaction):
        transaction.amount_fee = Utility.calculate_fee({
                        "amount": transaction.amount_in,
                        "operation": settings.OPERATION_WITHDRAWAL,
                        "asset_code": transaction.asset.code,
                    })

        try:
            self.__wallet.send_payment(transaction.to_address, transaction.amount_in - transaction.amount_fee, str(transaction.id))
            transaction.status = Transaction.STATUS.completed
            transaction.save()
        except:
            logger.error("An unexpected exception occurred while executing an outgoing transaction")
