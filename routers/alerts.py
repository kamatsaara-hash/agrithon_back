from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from utils.anomaly import detect_anomaly

router = APIRouter()

# ✅ Define request model
class PriceInput(BaseModel):
    prices: List[float]

# ✅ Endpoint
@router.post("/anomaly")
def anomaly(data: PriceInput):
    try:
        anomalies = detect_anomaly(data.prices)
        return {"anomalies": anomalies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))