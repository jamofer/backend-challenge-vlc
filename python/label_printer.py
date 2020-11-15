class LabelPrinter(object):
    queue = []

    @classmethod
    def print(cls, label_text):
        cls.queue.append(label_text)

    @classmethod
    def reset(cls):
        cls.queue = []
