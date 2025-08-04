import sys
import os
import traceback


class CustomException(Exception):
    def __init__(self, error_message:str,error_details:sys):
        self.error_message = error_message
        self.error_details = error_details

        _,_,exc_tb = error_details.exc_info()
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.line_number = exc_tb.tb_lineno
        self.error_message = str(error_message)
        self.traceback = ''.join(traceback.format_exception(*error_details.exc_info()))

    def __str__(self):
        return f"Error occurred in script: {self.file_name} at line number: {self.line_number} with message: {self.error_message} \nTraceback: {self.traceback}"

    if __name__ == "__main__":
        try:
            1 / 0  # Example to raise an exception
        except Exception as e:
            error = CustomException(e, sys)
            raise error