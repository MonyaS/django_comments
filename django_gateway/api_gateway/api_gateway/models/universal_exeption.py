class InternalException(Exception):
    """
    Class for internal exceptions that can be raised in any place of code
    and will be processed in the decorator exception_handler as an expected error.

    Fields:
        exception_data - error text
        exception_code - http code of the exception
    """

    def __int__(self, exception_data, exception_code):
        self.exception_data = exception_data
        self.exception_code: int = exception_code
        super().__init__("InternalException")
