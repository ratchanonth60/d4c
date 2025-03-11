class DatabaseError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        """
        Initialize the DatabaseError.

        Args:
            message (str): The error message describing the issue.
            status_code (int): HTTP status code (default: 500 for server errors).
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(Exception):
    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
