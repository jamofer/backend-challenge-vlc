class DiscountCodes:
    customer_discount_codes = {}

    @classmethod
    def by_customer(cls, customer):
        if customer not in cls.customer_discount_codes:
            return []

        return cls.customer_discount_codes[customer]

    @classmethod
    def add(cls, customer, code, percentage):
        if customer not in cls.customer_discount_codes:
            cls.customer_discount_codes[customer] = []

        cls.customer_discount_codes[customer].append(code)

    @classmethod
    def reset(cls):
        cls.customer_discount_codes = {}
