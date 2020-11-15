from datetime import datetime
from bootstrap import Payment, ProductType
from label_printer import LabelPrinter


def pay(order, payment_method):
    payment = Payment(order, payment_method, paid_at=datetime.now())
    order.payment = payment
    order.close(payment.paid_at)

    if order.has_physical_items:
        LabelPrinter.enqueue(_generate_shipping_label(order))


def _generate_shipping_label(order):
    return (
        f'Name: {order.customer.name}\n'
        f'ZipCode: {order.address.zipcode}\n'
    )
