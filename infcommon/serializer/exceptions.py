class DeserializeError(Exception):
    def __init__(self, exception, data):
        super().__init__(self, exception, data)
        self.exception = exception
        self.data = data
