from fastapi import APIRouter, UploadFile, File
import pandas as pd
from ml.data_analyzer import analyze_data

router = APIRouter(prefix="/api", tags=["Analyze"])

@router.post("/analyze")
async def analyze_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    result = analyze_data(df)
    return result