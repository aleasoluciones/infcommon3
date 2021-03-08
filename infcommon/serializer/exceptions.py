
class DeserializeError(Exception):
    def __init__(self, exception, data):
        super(DeserializeError, self).__init__(self, exception, data)
        self.exception = exception
        self.data = data
