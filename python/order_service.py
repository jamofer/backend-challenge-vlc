from datetime import datetime
from bootstrap import Payment


def pay(order, payment_method):
    payment = Payment(order, payment_method, paid_at=datetime.now())
    order.payment = payment
    order.close(payment.paid_at)
