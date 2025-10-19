from fastapi import APIRouter, Query
import pandas as pd
import io
from ml.inventory_predictor import json_inventory_data
from db import crud

router = APIRouter(prefix="/api", tags=["Predict"])

@router.get("/predict")
async def predict_inventory(
    email: str = Query(..., description="User email for data lookup"),
    days: int = Query(None, description="Optional number of days to forecast")
):
    # Get cleaned data from Supabase
    response = crud.get_clean(email)
    data = response.data

    if not data:
        return {"error": "No cleaned data found for this user"}

    latest_record = sorted(data, key=lambda x: x.get("created_at", ""))[-1]
    df_data = latest_record.get("cleaned_data")

    # Convert stored data back to DataFrame
    if isinstance(df_data, str):
        try:
            df = pd.DataFrame(eval(df_data))
        except Exception:
            df = pd.read_csv(io.StringIO(df_data))
    else:
        df = pd.DataFrame(df_data)

    # Run your inventory predictor
    prediction_result = json_inventory_data(df, days)
    summary = f"Predicted inventory for {len(prediction_result)} days."

    # Store predictions
    crud.insert_predict(
        email=email,
        file_name=latest_record.get("file_name", "unknown.csv"),
        df_json=prediction_result,
        summary=summary
    )

    return {
        "message": "Prediction successful",
        "summary": summary,
        "predicted_data": prediction_result
    }
