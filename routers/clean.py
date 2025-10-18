from fastapi import APIRouter, UploadFile, File
import pandas as pd
from ml.data_cleaner import clean_data

router = APIRouter(prefix="/api", tags=["Clean"])

@router.post("/clean")
async def clean_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    cleaned_df, summary = clean_data(df)
    cleaned_path = "cleaned_data.csv"
    cleaned_df.to_csv(cleaned_path, index=False)
    return {"message": "Data cleaned successfully!", "summary": summary}