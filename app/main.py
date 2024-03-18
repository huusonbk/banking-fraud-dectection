import os
from fastapi import FastAPI
from schema import TransactionInfo, TransactionPrediction
from utils.data_processing import format_input_data
from utils.logging import logger
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from utils.data_processing import Fraud
import joblib

# Creating FastAPI instance
app = FastAPI()

# Loading model with default path models/model.pkl
min_max_scaler_path = os.environ.get("MIN_MAX_PATH", "../models/minmaxscaler_cycle1.joblib")
one_hot_encoder_path = os.environ.get("ONE_HOT_PATH", "../models/onehotencoder_cycle1.joblib")
model_path = os.environ.get("MODEL_PATH", "../models/model_cycle1.joblib")
model = joblib.load(model_path)

# Creating an endpoint to receive the data
# to make prediction on
@app.post("/predict")
def predict(data: TransactionInfo):
    # Predicting the class
    logger.info("Make predictions...")
    # Convert data to pandas DataFrame and make predictions
    infer_data = format_input_data(data)
    # Instantiate Rossmann class
    pipeline = Fraud(min_max_scaler_path, one_hot_encoder_path)
    # data cleaning
    df1 = pipeline.data_cleaning(infer_data)
    # feature engineering
    df2 = pipeline.feature_engineering(df1)
    # data preparation
    df3 = pipeline.data_preparation(df2)
    # prediction
    is_fraud = pipeline.get_prediction(model, infer_data, df3)
    return {"is_fraud":is_fraud}





