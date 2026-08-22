import traceback # to track traceback error
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail:Exception):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail:Exception):
        exc_tb = error_detail.__traceback__

        error_type_name = type(error_detail).__name__

        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename  # file name where error occured
            line_no = exc_tb.tb_lineno  # line no where error occured
            return f"Error in [{file_name}] at line [{line_no}] -> {error_message}\nCause: [{error_type_name}]: {str(error_detail)}"

        return f"{error_message} | Cause: {str(error_detail)}"
    
    # Show the error
    def __str__(self):
        return self.error_message