class InternalException(Exception):
    """
    Class for internal exceptions that can be raised in any place of code
    and will be processed in the decorator exception_handler as an expected error.

    Fields:
        exception_data - error text
        answer_key - routing key that came with incoming message to route answer
    """

    def __int__(self, exception_data, answer_key: None):
        self.exception_data = exception_data
        self.answer_key = answer_key
        super().__init__("InternalException")
