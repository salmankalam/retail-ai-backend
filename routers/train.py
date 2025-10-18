from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Train"])

@router.post("/train")
def train_model():
    return {"message": "Training endpoint placeholder (future feature)."}