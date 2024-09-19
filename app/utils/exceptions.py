class ApplicationError(Exception):
    is_application_error = True

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


# Common error classes
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


class appForbiddenError(ApplicationError):
    def __init__(self, message='Access forbidden'):
        super().__init__(message, 403)


class appBadRequestError(ApplicationError):
    def __init__(self, message='Bad request'):
        super().__init__(message, 400)
