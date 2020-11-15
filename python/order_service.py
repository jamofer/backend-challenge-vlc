from datetime import datetime
from bootstrap import Payment, ProductType
from email_client import EmailClient
from label_printer import LabelPrinter
from subscriptions import Subscriptions


def pay(order, payment_method):
    payment = Payment(order, payment_method, paid_at=datetime.now())
    order.payment = payment
    order.close(payment.paid_at)

    if order.phyisical_items:
        LabelPrinter.enqueue(_generate_shipping_label(order))

    for item in order.membership_items:
        Subscriptions.activate(order.customer, item.product.name, item.quantity)
        EmailClient.send(
            order.customer.email,
            subject=f'{item.product.name} subscription',
            body=_generate_email_body(item, order)
        )


def _generate_email_body(item, order):
    return (
        f'Hello {order.customer.name}\n'
        f'You have been subscribed to "{item.product.name}" for {item.quantity} months\n'
    )


def _generate_shipping_label(order):
    return (
        f'Name: {order.customer.name}\n'
        f'ZipCode: {order.address.zipcode}\n'
    )
