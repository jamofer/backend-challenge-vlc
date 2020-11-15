from unittest import TestCase

from bootstrap import Order, Product, ProductType, Customer


class TestOrder(TestCase):
    def test_add_a_single_product(self):
        order = Order(Customer())
        order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10.0), 1)

        assert len(order.items) == 1

    def test_add_multiple_products(self):
        order = Order(Customer())
        order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10.0), 1)
        order.add_product(Product(name='Product 2', type=ProductType.BOOK, price=11.0), 1)
        order.add_product(Product(name='Product 3', type=ProductType.PHYSICAL, price=12.0), 1)

        assert len(order.items) == 3

    def test_add_two_of_a_single_product(self):
        order = Order(Customer())
        order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10.0), quantity=2)

        assert len(order.items) == 1

    def test_add_many_products_with_many_quantities(self):
        order = Order(Customer())
        order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10.0), quantity=1)
        order.add_product(Product(name='Product 2', type=ProductType.DIGITAL, price=10.0), quantity=3)
        order.add_product(Product(name='Product 3', type=ProductType.PHYSICAL, price=12.0), quantity=10)

        assert len(order.items) == 3

    def test_total_amount(self):
        order = Order(Customer())
        order.add_product(Product(name='Product 1', type=ProductType.DIGITAL, price=10), quantity=2)
        order.add_product(Product(name='Product 2', type=ProductType.DIGITAL, price=15), quantity=2)

        assert order.total_amount == 50
