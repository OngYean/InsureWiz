from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class InsureWizException(Exception):
    """Base exception for InsureWiz application"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class AIServiceException(InsureWizException):
    """Exception raised when AI service encounters an error"""
    
    def __init__(
        self,
        message: str = "AI service error occurred",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )

class VectorStoreException(InsureWizException):
    """Exception raised when vector store operations fail"""
    
    def __init__(
        self,
        message: str = "Vector store error occurred",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )

class ValidationException(InsureWizException):
    """Exception raised when data validation fails"""
    
    def __init__(
        self,
        message: str = "Validation error occurred",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )

class ConfigurationException(InsureWizException):
    """Exception raised when configuration is invalid"""
    
    def __init__(
        self,
        message: str = "Configuration error occurred",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )

def handle_insurewiz_exception(exc: InsureWizException) -> HTTPException:
    """Convert InsureWizException to FastAPI HTTPException"""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "message": exc.message,
            "details": exc.details,
            "error_type": exc.__class__.__name__
        }
    )

