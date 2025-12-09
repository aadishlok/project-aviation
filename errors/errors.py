class AppException(Exception):


    def __init__(self, message: str, code: str = "APP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationException(AppException):


    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")


class ExternalAPIException(AppException):

    
    def __init__(self, message: str):
        super().__init__(message, code="EXTERNAL_API_ERROR")
