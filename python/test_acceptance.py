from unittest import TestCase

from bootstrap import Customer, Product, Order, CreditCard, Payment, ProductType


class TestAcceptance(TestCase):
    def test_it_orders_a_book(self):
        foolano = Customer()
        book = Product(name='Awesome book', type=ProductType.BOOK, price=10.0)
        book_order = Order(foolano)
        book_order.add_product(book, 1)
        payment_attributes = dict(
            order=book_order,
            payment_method=CreditCard.fetch_by_hashed('43567890-987654367')
        )

        payment_book = Payment(attributes=payment_attributes)
        payment_book.pay()

        assert payment_book.is_paid
        assert payment_book.order.customer == foolano
        assert payment_book.order.items[0].product == book
