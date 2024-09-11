from models.universal_exeption import InternalException


class Message:
    """
        Message class describe incoming broker message entity.
    """

    AVAILABLE_METHODS = ["add", "get"]

    def __init__(self, **kwargs):
        self.headers = kwargs.get("headers", {})
        self.body = kwargs.get("body", None)

        # Headers parameters
        self.method = None
        self.answer_key = None

        # Comment object
        self.comment = None

        self._decode_headers()

    def _decode_headers(self):
        """
            Check the header of message.
        """
        if not self.headers:
            raise InternalException("Headers isn`t valid.", self.answer_key)
        self.method = self.headers.get("method")

        if self.method not in self.AVAILABLE_METHODS:
            raise InternalException("Unpronounceable method.", self.answer_key)

        self.answer_key = self.headers.get("answer_key")
