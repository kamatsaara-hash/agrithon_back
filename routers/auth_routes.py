from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import users
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------
# 📦 Schemas
# -----------------------------
class SignupInput(BaseModel):
    role: str
    email: str | None = None
    phone: str | None = None
    password: str


class LoginInput(BaseModel):
    role: str
    email: str | None = None
    phone: str | None = None
    password: str


# -----------------------------
# 📝 SIGNUP
# -----------------------------
@router.post("/signup")
def signup(data: SignupInput):

    if not data.email and not data.phone:
        raise HTTPException(status_code=400, detail="Provide email or phone")

    # Build query dynamically
    query = {"role": data.role}
    if data.email:
        query["email"] = data.email
    if data.phone:
        query["phone"] = data.phone

    existing_user = users.find_one(query)

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(data.password)

    user = {
        "role": data.role,
        "email": data.email,
        "phone": data.phone,
        "password": hashed_password
    }

    users.insert_one(user)

    return {"message": "Signup successful"}


# -----------------------------
# 🔓 LOGIN
# -----------------------------
@router.post("/login")
def login(data: LoginInput):

    if not data.email and not data.phone:
        raise HTTPException(status_code=400, detail="Provide email or phone")

    # Build query dynamically
    query = {"role": data.role}
    if data.email:
        query["email"] = data.email
    if data.phone:
        query["phone"] = data.phone

    user = users.find_one(query)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "message": "Login successful",
        "role": user["role"]
    }