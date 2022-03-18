import requests
import json

import PyEasyQiwi.qiwi_service.support_module as support_module
from PyEasyQiwi.errors import *

__all__ = [
    'QiwiConnection'
    ]


class QiwiConnection:
    """
    Main class for create QIWI connection object

    > > >   x = QiwiConnection(key)

    key:<string> - Your secret P2P QIWI key
    """

    def __init__(self, key):
        """Constructor class"""
        if key is None:
            raise QiwiInvalidToken("Invalid QIWI token!")
        self.key = str(key)

    def create_bill(self, value, currency="RUB", delay=15, description="unknown", theme_code="unknown", comment="", qiwi_pay=True, card_pay=True):
        """
        The method for creating a new invoice for payment in the QIWI service,
        use this for each new customer purchase, unfortunately,
        this library does not allow you to receive an automatic
        response with the status - check the documentation for
        checking the status of the invoice.

        Arguments:
            *REQUIRED*
            value:<float> (1-1000000) - Value of the amount to be paid

            *NON-REQUIRED*
            currency:<string> (RUB, KZT) - Currency name, default = 'RUB'
            delay:<int> (>=1) - Time to pay the invoice, after the expiration of the invoice will be overdue, default = 15
            description:<string> (max 50) - Name for the payment ID, default = 'unknown'
            theme_code:<string> -  Your personal account appearance code check the QIWI settings, default = 'unknown'
            comment:<string> (max 255) - Description on the payment page for customers, default = ''
            qiwi_pay:<bool> - Ability to use QIWI wallet payment, default = True
            card_pay:<bool> - The ability to use a bank card payment, default = True

        Response:
            pay_url:<string> - Payment link for customers
            bill_id:<string> - ID for receiving information about the payment status
            response:<dict> - More information about the payment


          """

        if len(str(description)) > 50:
            raise QiwiTooLongDescription("Description is too long, max 50 symbols!")

        description = description.replace(" ", "-")

        if delay is int or int(delay) >= 1:
            pass
        else:
            raise QiwiInvalidDelay("Invalid delay value, (<int> >= 1)")

        if value is float or 1 <= float(value) <= 1000000:
            pass
        else:
            raise QiwiInvalidAmountValue("Invalid amount:value for QIWI, (1-1000000)!")

        if len(str(comment)) > 256:
            raise QiwiTooLongComment("Comment is too long, max 255 symbols!")

        pay_source = ""
        if qiwi_pay:
            pay_source = "qw"
        if card_pay:
            pay_source = "card"
        if qiwi_pay and card_pay:
            pay_source = "card, qw"
        if not qiwi_pay and not card_pay:
            raise QiwiPaymentMethodNotSelected("Аt least one value must be true (card_pay, qiwi_pay)")

        datetime_link, datetime_expiration = support_module.create_datetime_link_and_expiration(int(delay))
        bill_id = str(description) + datetime_link
        create_url = "https://api.qiwi.com/partner/bill/v1/bills/" + bill_id

        parameters = json.dumps({'amount': {'value': round(float(value), 2), 'currency': currency},
                                 'expirationDateTime': datetime_expiration,
                                 'customFields': {'themeCode': theme_code, 'paySourcesFilter': pay_source},
                                 'comment': str(comment)
                                 })

        session = requests.Session()
        session.headers['authorization'] = 'Bearer ' + self.key
        session.headers['content-type'] = 'application/json'
        session.headers['accept'] = 'application/json'

        response = session.put(create_url, data=parameters)

        return str(response.json()['payUrl']), bill_id, str(response.json())

    def check_bill(self, bill_id):
        """
        The method for checking the status of the invoice,
        use to verify the payment in your application.

        Available statuses:
        WAITING - Invoice issued, awaiting payment
        PAID - The invoice is paid
        REJECTED - The invoice is rejected
        EXPIRED - The account's lifetime has expired. The bill has not been paid

        Arguments:
            *REQUIRED*
            bill_id:<string> - Bill ID for check

        Response:
            status:<string> - Status of the invoice issued
            response:<dict> - More information about the payment
        """

        if bill_id and bill_id != "":
            pass
        else:
            raise QiwiInvalidBillId("Bill ID can't be empty!")

        check_url = "https://api.qiwi.com/partner/bill/v1/bills/" + str(bill_id)

        session = requests.Session()
        session.headers['authorization'] = 'Bearer ' + self.key
        session.headers['accept'] = 'application/json'
        response = session.get(check_url)

        return str(response.json()['status']['value']), str(response.json())

    def remove_bill(self, bill_id):
        """
        The method for canceling the invoice, if the client refuses,
        is the best practice to close the invoice for payment yourself.
        This will help to avoid erroneous payments.

        Arguments:
            *REQUIRED*
            bill_id:<string> - Bill ID for check

        Response:
            None
        """

        if bill_id and bill_id != "":
            pass
        else:
            raise QiwiInvalidBillId("Bill ID can't be empty!")

        remove_url = 'https://api.qiwi.com/partner/bill/v1/bills/' + bill_id + "/reject"

        session = requests.Session()
        session.headers['authorization'] = 'Bearer ' + self.key
        session.headers['content-type'] = 'application/json'
        session.headers['accept'] = 'application/json'

        response = session.post(remove_url)