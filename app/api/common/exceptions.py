class UserCreationError(Exception):
    """Exception raised for errors in the database when AuthUser is created."""

    def __init__(self):
        self.message = "Error when creating AuthUser instance with username: {}"
        super().__init__(self.message)


class CustomerUpdateError(Exception):
    """Exception raised for errors in the database when Customer is updated."""

    def __init__(self):
        self.message = "Error when creating Customer instance with email: {}"
        super().__init__(self.message)
