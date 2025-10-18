from fastapi import APIRouter, UploadFile, File, Query
import pandas as pd
from ml.forecast_model import predict_demand

router = APIRouter(prefix="/api", tags=["Predict"])

@router.post("/predict")
async def predict(file: UploadFile = File(...), days: int = Query(7)):
    df = pd.read_csv(file.file)
    results = predict_demand(df, days)
    return results