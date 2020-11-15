from unittest import TestCase

import order_service
from bootstrap import Customer, Product, Order, CreditCard, ProductType, Address
from email_client import Mail, EmailClient
from label_printer import LabelPrinter
from subscriptions import Subscriptions


class TestAcceptance(TestCase):
    def tearDown(self):
        LabelPrinter.reset()
        EmailClient.reset()
        Subscriptions.reset()

    def test_it_orders_a_book(self):
        foolano = Customer('Foolano')
        foolanos_credit_card = CreditCard.fetch_by_hashed('43567890-987654367')
        book = Product(name='Awesome book', type=ProductType.BOOK, price=10.0)
        book_order = Order(foolano)
        book_order.add_product(book, 1)

        order_service.pay(book_order, payment_method=foolanos_credit_card)

        assert book_order.is_paid
        assert book_order.customer == foolano
        assert book_order.items[0].product == book
        assert book_order.payment.amount == 10.0

    def test_it_orders_a_physical_item(self):
        expected_shipping_label = (
            'Name: Antonio\n'
            'ZipCode: 46100\n'
       )
        customer = Customer('Antonio')
        credit_card = CreditCard.fetch_by_hashed('43567890-987654367')
        item = Product(name='Awesome bottle', type=ProductType.PHYSICAL, price=15.0)
        order = Order(customer, Address('46100'))
        order.add_product(item, 1)

        order_service.pay(order, payment_method=credit_card)

        assert order.is_paid
        assert order.customer == customer
        assert order.items[0].product == item
        assert order.payment.amount == 15.0
        assert expected_shipping_label in LabelPrinter.queue

    def test_it_orders_a_service_subscription_item(self):
        expected_mail = Mail(
            address='bill.gates@hotmail.com',
            subject='Netflix subscription',
            body=(
                'Hello Cuenta Puertas\n'
                'You have been subscribed to "Netflix" for 2 months\n'
            )
        )
        customer = Customer('Cuenta Puertas', email='bill.gates@hotmail.com')
        credit_card = CreditCard.fetch_by_hashed('43567890-987654367')
        item = Product(name='Netflix', type=ProductType.MEMBERSHIP, price=15.0)
        order = Order(customer, Address('46100'))
        order.add_product(item, 2)

        order_service.pay(order, payment_method=credit_card)

        assert order.is_paid
        assert order.customer == customer
        assert order.items[0].product == item
        assert order.payment.amount == 30.0
        assert expected_mail in EmailClient.queue
        assert 'Netflix' in Subscriptions.by_customer(customer)
