class Comment:

    """
        Comment class describe comment entity.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.parent_id = kwargs.get("parent_id")
        self.user_id = kwargs.get("user_id")
        self.text = kwargs.get("text")
        self.home_page = kwargs.get("home_page", "/")
