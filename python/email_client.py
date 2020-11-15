class Mail(object):
    def __init__(self, address, subject, body):
        self.address = address
        self.subject = subject
        self.body = body

    def __eq__(self, other):
        return (
            self.address == other.address and
            self.subject == other.subject and
            self.body == other.body
        )


class EmailClient(object):
    queue = []

    @classmethod
    def send(cls, address, subject='', body=''):
        cls.queue.append(Mail(address, subject, body))

    @classmethod
    def reset(cls):
        cls.queue = []
