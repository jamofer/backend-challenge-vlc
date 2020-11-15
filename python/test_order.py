from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

import order_service
from bootstrap import Order, Product, ProductType, Customer, CreditCard, Payment, Invoice


class TestOrder(TestCase):
    def setUp(self):
        self.datetime = patch('order_service.datetime').start()
        self.order = Order(Customer())

    def tearDown(self):
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
