class Comment:
    """
        Comment class describe comment entity.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.parent_id = kwargs.get("parent_id", None)
        self.user_id = kwargs.get("user_id")
        self.text = kwargs.get("text")
        self.home_page = kwargs.get("home_page", "/")

    @property
    def __dict__(self):
        return {"user_id": self.user_id, "text": self.text, "home_page": self.home_page, "children": []}
