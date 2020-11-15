import time
from enum import Enum


class Payment:
    def __init__(self, order, payment_method):
        self.order = order
        self.payment_method = payment_method
        self.authorization_number = None
        self.amount = None
        self.invoice = None
        self.paid_at = None

    def pay(self, paid_at=time.time()):
        self.amount = self.order.total_amount
        self.authorization_number = int(time.time())
        attributes = dict(
            billing_address=self.order.address,
            shipping_address=self.order.address,
            order=self.order
        )
        self.invoice = Invoice(attributes=attributes)
        self.paid_at = paid_at
        self.order.close(self.paid_at)

    @property
    def is_paid(self):
        return self.paid_at is not None


class Invoice:
    def __init__(self, attributes={}):
        self.billing_address = attributes.get('billing_address', None)
        self.shipping_address = attributes.get('shipping_address', None)
        self.order = attributes.get('order', None)


class Address:
    def __init__(self, zipcode):
        self.zipcode = zipcode


class Order:
    def __init__(self, customer, address=Address(zipcode='45678-979')):
        self.customer = customer
        self.address = address
        self.items = []
        self.payment = None
        self.closed_at = None

    def add_product(self, product, quantity):
        self.items.append(OrderItem(product=product, quantity=quantity))

    @property
    def total_amount(self):
        return sum(item.total for item in self.items)

    def close(self, closed_at=time.time()):
        self.closed_at = closed_at

    # remember: you can create new methods inside those classes to help you create a better design


class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    @property
    def total(self):
        return self.product.price * self.quantity


class ProductType(Enum):
    PHYSICAL = 'physical'
    BOOK = 'book'
    DIGITAL = 'digital'
    MEMBERSHIP = 'membership'


class Product:
    # use type to distinguish each kind of product: physical, book, digital, membership, etc.
    def __init__(self, name, type, price):
        self.name = name
        self.type = type
        self.price = price


class CreditCard:
    @staticmethod
    def fetch_by_hashed(code):
        return CreditCard()


class Customer:
    # you can customize this class by yourself
    pass


class Membership:
    # you can customize this class by yourself
    pass
