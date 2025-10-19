from fastapi import APIRouter, UploadFile, File, Query
import pandas as pd
from ml.data_cleaner import clean_data
from db import crud

router = APIRouter(prefix="/api", tags=["Clean"])

@router.post("/clean")
async def clean_csv(file: UploadFile = File(...), email: str = Query("guest@example.com")):
    df = pd.read_csv(file.file)
    cleaned_df, summary = clean_data(df)

    # Save to Supabase via CRUD
    crud.insert_clean(email=email, file_name=file.filename, df=cleaned_df)

    return {
        "message": "Data cleaned successfully!",
        "rows": len(cleaned_df),
        "summary": summary
    }

@router.get("/clean")
async def get_clean(email: str = Query("guest@example.com")):
    res = crud.get_clean(email)
    return {"records": res.data}
