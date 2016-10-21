class User():
    """The main user class.

    variables:
    id - id of the user
    username - username of the user
    is_admin - boolean whether the user is an administrator or not
    """

    def __init__(self, id, username, is_admin):
        self.id = id
        self.username = username
        self.is_admin = is_admin
