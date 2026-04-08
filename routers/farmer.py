from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from database import crops
from utils.price_model import predict_price
from utils.profit import calculate_profit

router = APIRouter()

# -----------------------------
# 📦 Schemas
# -----------------------------

class CropInput(BaseModel):
    name: str
    price: float
    quantity: int
    farmer_id: str


class PriceInput(BaseModel):
    commodity: str
    history: List[float]


class ProfitInput(BaseModel):
    cost: float
    predicted_price: float


# -----------------------------
# 🌾 Add Crop
# -----------------------------
@router.post("/add-crop")
def add_crop(crop: CropInput):
    crops.insert_one(crop.dict())
    return {
        "message": "Crop added successfully",
        "data": crop
    }


# -----------------------------
# 📈 Price Insights (Random Forest)
# -----------------------------
@router.post("/price-insights")
def price_insights(data: PriceInput):
    history = data.history

    # 🔒 Basic validation
    if len(history) < 2:
        return {"error": "At least 2 price values required"}

    # Predict using Random Forest
    predicted = predict_price(history)

    # Handle model error
    if isinstance(predicted, dict):
        return predicted

    current_price = history[-1]

    # 🔥 Smart suggestion logic
    if predicted > current_price * 1.05:
        suggestion = "Sell"
    elif predicted < current_price * 0.95:
        suggestion = "Hold"
    else:
        suggestion = "Stable"

    return {
        "commodity": data.commodity,
        "current_price": current_price,
        "predicted_price": round(predicted, 2),
        "suggestion": suggestion
    }


# -----------------------------
# 💰 Profit Calculation
# -----------------------------
@router.post("/profit")
def profit(data: ProfitInput):
    profit_value = calculate_profit(data.cost, data.predicted_price)

    roi = (profit_value / data.cost) * 100 if data.cost > 0 else 0

    return {
        "cost": data.cost,
        "predicted_price": data.predicted_price,
        "profit": round(profit_value, 2),
        "roi_percentage": round(roi, 2)
    }