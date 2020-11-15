from datetime import datetime
from bootstrap import Payment
from discount_codes import DiscountCodes
from email_client import EmailClient
from label_printer import LabelPrinter
from subscriptions import Subscriptions


DIGITAL_PURCHASE_DISCOUNT_PERCENTAGE = 10


def pay(order, payment_method):
    payment = Payment(order, payment_method, paid_at=datetime.now())
    order.payment = payment
    order.close(payment.paid_at)

    if order.physical_items:
        LabelPrinter.enqueue(_generate_shipping_label(order))

    if order.book_items:
        LabelPrinter.enqueue(_generate_shipping_label(order, tax_exempt=True))

    for item in order.membership_items:
        Subscriptions.activate(order.customer, item.product.name, item.quantity)
        EmailClient.send(
            order.customer.email,
            subject=f'{item.product.name} subscription',
            body=_subscription_mail(order.customer, item)
        )

    for item in order.digital_items:
        code = _random_code()
        DiscountCodes.add(order.customer, code, percentage=DIGITAL_PURCHASE_DISCOUNT_PERCENTAGE)
        EmailClient.send(
            order.customer.email,
            subject='Purchase details',
            body=_purchase_mail(order.customer, item, code)
        )


def _random_code():
    return 'ABC1234'


def _subscription_mail(customer, item):
    return (
        f'Hello {customer.name}\n'
        f'You have been subscribed to "{item.product.name}" for {item.quantity} months\n'
    )


def _purchase_mail(customer, item, code):
    return (
        f'Hello {customer.name}\n'
        f'You have purchased "{item.product.name}"\n'
        f'Use the following code for a {DIGITAL_PURCHASE_DISCOUNT_PERCENTAGE}% discount in the next order:\n'
        f'{code}\n'
    )


def _generate_shipping_label(order, tax_exempt=False):
    label = (
        f'Name: {order.customer.name}\n'
        f'ZipCode: {order.address.zipcode}\n'
    )
    if tax_exempt:
        label += '** Tax exempt **\n'

    return label
