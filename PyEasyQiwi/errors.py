class QiwiInvalidToken(Exception):
    pass


class QiwiInvalidAmountValue(Exception):
    pass


class QiwiTooLongComment(Exception):
    pass


class QiwiTooLongDescription(Exception):
    pass


class QiwiPaymentMethodNotSelected(Exception):
    pass


class QiwiInvalidDelay(Exception):
    pass


class QiwiInvalidBillId(Exception):
    pass