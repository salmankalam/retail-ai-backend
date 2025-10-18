from fastapi import FastAPI, HTTPException, Form
from routers import analyze, clean, predict, train, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Retail-AI-Predict")

# Add this section to allow frontend
origins = [
    "http://localhost:3000",   # your Next.js app
    "http://127.0.0.1:3000",   # sometimes needed separately
    "http://127.0.0.1:5500",
    "https://forecast-x.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # or restrict to ["POST", "GET"] for security
    allow_headers=["*"],
)

app.include_router(analyze.router)
app.include_router(clean.router)
app.include_router(predict.router)
app.include_router(train.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Retail-AI-Predict API running!"}