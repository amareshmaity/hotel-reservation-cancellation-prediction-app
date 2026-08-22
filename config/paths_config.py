import os

############## DATA INGESTION ################
RAW_DATA_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DATA_DIR, "raw.csv")
TRAIN_DATA_FILE_PATH = os.path.join(RAW_DATA_DIR, "train.csv")
TEST_DATA_FILE_PATH = os.path.join(RAW_DATA_DIR, "test.csv")

CONFIG_PATH = "config/config.yaml"


################# DATA PROCESSING #################
PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")


################# MODEL TRAINING #################
MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl"