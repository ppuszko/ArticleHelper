from fastapi import status

class AppException(Exception):
    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)

class BadRequest(AppException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

class InternalServerError(AppException):
    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LLMError(AppException):
    def __init__(self, detail: str = "LLM processing error. Please try again later."):
        super().__init__(detail=detail, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

class ServiceMissingError(AppException):
    def __init__(self, detail: str = "Configuration error"):
        super().__init__(detail=detail, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

class ConfigurationError(AppException):
    def __init__(self, detail: str = "Configuration error"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)