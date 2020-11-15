class Subscriptions:
    customer_subscriptions = {}

    @classmethod
    def by_customer(cls, customer):
        if customer not in cls.customer_subscriptions:
            return []

        return cls.customer_subscriptions[customer]

    @classmethod
    def activate(cls, customer, name, quantity):
        if customer not in cls.customer_subscriptions:
            cls.customer_subscriptions[customer] = []

        cls.customer_subscriptions[customer].append(name)

    @classmethod
    def reset(cls):
        cls.customer_subscriptions = {}
