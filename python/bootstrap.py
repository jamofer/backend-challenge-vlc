import time
from enum import Enum


class Payment:
    authorization_number = None
    amount = None
    invoice = None
    order = None
    payment_method = None
    paid_at = None

    def __init__(self, attributes={}):
        self.authorization_number = attributes.get('attributes', None)
        self.amount = attributes.get('amount', None)
        self.invoice = attributes.get('invoice', None)
        self.order = attributes.get('order', None)
        self.payment_method = attributes.get('payment_method', None)

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
    billing_address = None
    shipping_address = None
    order = None

    def __init__(self, attributes={}):
        self.billing_address = attributes.get('billing_address', None)
        self.shipping_address = attributes.get('shipping_address', None)
        self.order = attributes.get('order', None)


class Order:
    customer = None
    items = None
    payment = None
    address = None
    closed_at = None

    def __init__(self, customer, attributes={}):
        self.customer = customer
        self.items = []
        self.order_item_class = attributes.get('order_item_class', OrderItem)
        self.address = attributes.get('address', Address(zipcode='45678-979'))

    def add_product(self, product, quantity):
        self.items.append(self.order_item_class(product=product, quantity=quantity))

    @property
    def total_amount(self):
        total = 0
        for item in self.items:
            total += item.total()

        return total

    def close(self, closed_at=time.time()):
        self.closed_at = closed_at

    # remember: you can create new methods inside those classes to help you create a better design


class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

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


class Address:
    zipcode = None

    def __init__(self, zipcode):
        self.zipcode = zipcode


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
