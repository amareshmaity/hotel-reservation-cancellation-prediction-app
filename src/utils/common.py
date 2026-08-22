import pandas as pd
import os
from src.custom_exception import CustomException
from src.utils.logger import get_logger
import yaml

logger = get_logger(__name__)


## Function to read yaml file
def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file is not found in the given path {file_path}")

        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read the YAML file")
            return config

    except Exception as e:
        logger.error("Error when reading the YAML file")
        raise CustomException("Failed to read YAML file", e)



## Function to load data
def load_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading the data {e}")
        raise CustomException("Failed to load data", e)