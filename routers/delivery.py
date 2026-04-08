from fastapi import APIRouter

router = APIRouter()

@router.get("/deliveries")
def deliveries():
    return {"orders": "List of available deliveries"}