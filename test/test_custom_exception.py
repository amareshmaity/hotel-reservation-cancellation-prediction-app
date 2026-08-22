import sys
from src.utils.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

def divide_number(a, b):
    try:
        result = a/b
        logger.info("dividing two numbers")
        return result
    except Exception as e:
        logger.error("Error occured")
        raise CustomException("divide by zero", sys)



if __name__ == '__main__':
    try:
        logger.info("starting program")
        divide_number(10,0)
    except CustomException as ce:
        logger.error(ce)