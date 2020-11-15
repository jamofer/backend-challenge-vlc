import time
from enum import Enum


class Payment:
    def __init__(self, order, payment_method, paid_at):
        self.authorization_number = int(time.time())
        self.payment_method = payment_method
        self.amount = order.total_amount
        self.paid_at = paid_at
        self.invoice = Invoice(
            billing_address=order.address,
            shipping_address=order.address,
        )


class Invoice:
    def __init__(self, billing_address=None, shipping_address=None):
        self.billing_address = billing_address
        self.shipping_address = shipping_address

    def __eq__(self, other):
        return (
            self.billing_address == other.billing_address and
            self.shipping_address == other.shipping_address
        )


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
    def is_paid(self):
        return self.payment is not None

    @property
    def total_amount(self):
        return sum(item.total for item in self.items)

    @property
    def phyisical_items(self):
        return [item for item in self.items if item.product.type == ProductType.PHYSICAL]

    @property
    def membership_items(self):
        return [item for item in self.items if item.product.type == ProductType.MEMBERSHIP]

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


class Customer(object):
    def __init__(self, name, email=None):
        self.name = name
        self.email = email

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.email == other.email
        )

    def __hash__(self):
        return hash((self.name, self.email))


class Membership:
    # you can customize this class by yourself
    pass
