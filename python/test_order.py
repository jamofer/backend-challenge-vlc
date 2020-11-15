from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

import order_service
from bootstrap import Order, Product, ProductType, Customer, CreditCard, Invoice, Address
from discount_codes import DiscountCodes
from email_client import EmailClient, Mail
from label_printer import LabelPrinter
from subscriptions import Subscriptions


class TestOrder(TestCase):
    def setUp(self):
        self.datetime = patch('order_service.datetime').start()
        self.order = Order(Customer('Antonio'))

    def tearDown(self):
        LabelPrinter.reset()
        EmailClient.reset()
        Subscriptions.reset()
        DiscountCodes.reset()
        patch.stopall()

    def test_add_a_single_product(self):
        self.order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10.0), 1)

        assert len(self.order.items) == 1

    def test_add_multiple_products(self):
        self.order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10.0), 1)
        self.order.add_product(Product(name='Product 2', type=ProductType.BOOK, price=11.0), 1)
        self.order.add_product(Product(name='Product 3', type=ProductType.PHYSICAL, price=12.0), 1)

        assert len(self.order.items) == 3

    def test_add_two_of_a_single_product(self):
        self.order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10.0), quantity=2)

        assert len(self.order.items) == 1

    def test_add_many_products_with_many_quantities(self):
        self.order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10.0), quantity=1)
        self.order.add_product(Product(name='Product 2', type=ProductType.DIGITAL, price=10.0), quantity=3)
        self.order.add_product(Product(name='Product 3', type=ProductType.PHYSICAL, price=12.0), quantity=10)

        assert len(self.order.items) == 3

    def test_total_amount(self):
        self.order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10), quantity=2)
        self.order.add_product(Product(name='Product 2', type=ProductType.DIGITAL, price=15), quantity=2)

        assert self.order.total_amount == 50

    def test_pay_order(self):
        self.datetime.now.return_value = datetime(2020, 1, 1)
        credit_card = CreditCard.fetch_by_hashed('01234-4321')
        self.order.add_product(Product('Untitled', ProductType.BOOK, price=20), quantity=10)

        order_service.pay(self.order, payment_method=credit_card)

        assert self.order.is_paid
        assert self.order.payment.paid_at == datetime(2020, 1, 1)
        assert self.order.payment.amount == 200
        assert self.order.payment.invoice == Invoice(self.order.address, self.order.address)

    def test_pay_order_with_physical_item(self):
        expected_label = (
            'Name: Manuela\n'
            'ZipCode: 46100\n'
        )
        credit_card = CreditCard.fetch_by_hashed('01234-4321')
        order = Order(Customer('Manuela'), Address('46100'))
        order.add_product(Product('Untitled', ProductType.PHYSICAL, price=20), quantity=10)

        order_service.pay(order, credit_card)

        assert expected_label in LabelPrinter.queue

    def test_pay_order_with_subscription(self):
        expected_mail = Mail(
            address='ophelia@gmail.com',
            subject='24/7 sl terminal show subscription',
            body=(
                'Hello Ofelia\n'
                'You have been subscribed to "24/7 sl terminal show" for 12 months\n'
            )
        )
        customer = Customer('Ofelia', 'ophelia@gmail.com')
        credit_card = CreditCard.fetch_by_hashed('01234-4321')
        order = Order(customer, Address('42100'))
        order.add_product(Product('24/7 sl terminal show', ProductType.MEMBERSHIP, price=20), quantity=12)

        order_service.pay(order, credit_card)

        assert expected_mail in EmailClient.queue
        assert '24/7 sl terminal show' in Subscriptions.by_customer(customer)

    def test_pay_order_with_book_item(self):
        expected_label = (
            'Name: Manuela\n'
            'ZipCode: 46100\n'
            '** Tax exempt **\n'
        )
        credit_card = CreditCard.fetch_by_hashed('01234-4321')
        order = Order(Customer('Manuela'), Address('46100'))
        order.add_product(Product('Untitled', ProductType.BOOK, price=20), quantity=10)

        order_service.pay(order, credit_card)

        assert expected_label in LabelPrinter.queue

    def test_pay_order_with_digital_item(self):
        expected_mail = Mail(
            address='asd@hotmail.com',
            subject='Purchase details',
            body=(
                'Hello Asd\n'
                'You have purchased "Need for Acceleration"\n'
                'Use the following code for a 10% discount in the next order:\n'
                'ABC1234\n'
            )
        )
        customer = Customer('Asd', 'asd@hotmail.com')
        credit_card = CreditCard.fetch_by_hashed('01234-4321')
        order = Order(customer)
        order.add_product(Product('Need for Acceleration', ProductType.DIGITAL, price=20), quantity=1)

        order_service.pay(order, credit_card)

        assert expected_mail in EmailClient.queue
        assert 'ABC1234' in DiscountCodes.by_customer(customer)

    def test_pay_order_with_digital_items(self):
        expected_mail = Mail(
            address='asd@hotmail.com',
            subject='Purchase details',
            body=(
                'Hello Asd\n'
                'You have purchased "Need for Acceleration", "Fogata Artica"\n'
                'Use the following code for a 10% discount in the next order:\n'
                'ABC1234\n'
            )
        )
        customer = Customer('Asd', 'asd@hotmail.com')
        credit_card = CreditCard.fetch_by_hashed('01234-4321')
        order = Order(customer)
        order.add_product(Product('Need for Acceleration', ProductType.DIGITAL, price=20), quantity=1)
        order.add_product(Product('Fogata Artica', ProductType.DIGITAL, price=30), quantity=1)

        order_service.pay(order, credit_card)

        assert expected_mail in EmailClient.queue
        assert 'ABC1234' in DiscountCodes.by_customer(customer)
