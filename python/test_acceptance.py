from unittest import TestCase

import order_service
from bootstrap import Customer, Product, Order, CreditCard, Payment, ProductType


class TestAcceptance(TestCase):
    def test_it_orders_a_book(self):
        foolano = Customer()
        foolanos_credit_card = CreditCard.fetch_by_hashed('43567890-987654367')
        book = Product(name='Awesome book', type=ProductType.BOOK, price=10.0)
        book_order = Order(foolano)
        book_order.add_product(book, 1)

        order_service.pay(book_order, payment_method=foolanos_credit_card)

        assert book_order.is_paid
        assert book_order.customer == foolano
        assert book_order.items[0].product == book
        assert book_order.payment.amount == 10.0
