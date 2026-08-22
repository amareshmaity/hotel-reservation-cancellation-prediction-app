import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.utils.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from src.utils.common import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.bucket_file_name = self.config['bucket_file_name']
        self.test_ratio = self.config['test_ratio']

        os.makedirs(RAW_DATA_DIR, exist_ok=True)

        logger.info(f"Data ingestion started with {self.bucket_name} and file is {self.bucket_file_name}")

    def download_csv(self):
        """Download csv data file from GCP"""
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name=self.bucket_file_name)

            blob.download_to_filename(filename=RAW_FILE_PATH)

            logger.info(f"Raw file is successfully downloaded to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while downloading the csv file")
            raise CustomException("Failed to download the csv file", e)

    def split_data(self):
        try:
            logger.info("Starting the splitting process")

            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=self.test_ratio, random_state=42)

            train_data.to_csv(TRAIN_DATA_FILE_PATH)
            test_data.to_csv(TEST_DATA_FILE_PATH)

            logger.info(f"Train data save to {TRAIN_DATA_FILE_PATH}")
            logger.info(f"Test data save to {TEST_DATA_FILE_PATH}")


        except Exception as e:
            logger.error("Error while splitting the csv file")
            raise CustomException("Failed to splitting the data into train and test set", e)


    def run(self):
        try:
            logger.info("Starting data ingestion process")

            self.download_csv()
            self.split_data()

            logger.info("Data ingestion completed successfully")

        except CustomException as ce:
            logger.error(f"Custom Exception: {str(ce)}")

        finally:
            logger.info("Data ingestion completed")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()