class ApplicationError(Exception):
    is_application_error = True

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


class appNotFoundError(ApplicationError):
    def __init__(self, message='Resource not found'):
        super().__init__(message, 404)


class appConflictError(ApplicationError):
    def __init__(self, message='Conflict occurred'):
        super().__init__(message, 409)


class appLoginError(ApplicationError):
    def __init__(self, message='Login failed'):
        super().__init__(message, 401)


class appProfileError(ApplicationError):
    def __init__(self, message='Profile not found'):
        super().__init__(message, 404)
