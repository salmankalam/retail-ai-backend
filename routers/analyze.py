from fastapi import APIRouter, UploadFile, File, Query
import pandas as pd
from ml.data_analyzer import analyze_data
from db import crud

router = APIRouter(prefix="/api", tags=["Analyze"])

@router.post("/analyze")
async def analyze_csv(file: UploadFile = File(...), user_id: str = Query("guest")):
    df = pd.read_csv(file.file)
    result = analyze_data(df)

    crud.insert_analyze(
        user_id=user_id,
        file_name=file.filename,
        df=df,
        summary=result
    )

    return {"message": "Data analyzed and saved successfully", "summary": result}


@router.get("/analyze")
async def get_analyzed_data(user_id: str = Query("guest")):
    res = crud.get_analyze(user_id)
    return {"records": res.data}
