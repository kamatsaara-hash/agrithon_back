from fastapi import APIRouter
from database import crops

router = APIRouter()

@router.get("/browse")
def browse():
    return list(crops.find({}, {"_id": 0}))