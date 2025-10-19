from fastapi import APIRouter, HTTPException, Form
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/api", tags=["Auth"])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def verify_password(plain_password: str, db_password: str):
    """Simple password check (plaintext) — upgrade later with hashing."""
    return plain_password == db_password


@router.post("/signup")
def signup(email: str = Form(...), password: str = Form(...)):
    """Registers a new user if email not already used."""
    existing = supabase.table("users").select("*").eq("email", email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    supabase.table("users").insert({"email": email, "password": password}).execute()
    return {"message": "User registered successfully", "user_email": email}


@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    """Verifies user login credentials."""
    res = supabase.table("users").select("*").eq("email", email).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user = res.data[0]
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful", "user_email": email}
