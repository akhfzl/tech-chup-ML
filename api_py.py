import joblib
from fastapi import FastAPI
from api_apps.base import PredictionRequest
import api_apps.utils as utils

app = FastAPI()
model = joblib.load("models/section3_rf_model.joblib")

@app.post("/predict_wait_time")
async def predictor(request: PredictionRequest):
    prediction = utils.predict(request, model)

    return {'predicted_wait_time': prediction}