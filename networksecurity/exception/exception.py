import sys

from networksecurity.logging.logger import logger

class NetworkSecurityException(Exception):
    """
    Custom exception class for network security-related errors.
    """
    def __init__(self, error_message, error_details=sys):
        super().__init__(error_message)
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.line_number = exc_tb.tb_lineno if exc_tb else None
        self.file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else None

    def __str__(self):
        return f"NetworkSecurityException: {self.error_message}"


