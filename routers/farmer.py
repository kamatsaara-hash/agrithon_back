from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
import os

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
# 🌾 Add Crop (MERGED VERSION)
# -----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/add-crop")
async def add_crop(
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    farmer_id: str = Form(...),
    image: UploadFile = File(...)
):
    # Save image
    file_path = os.path.join(UPLOAD_FOLDER, image.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())

    # Combine both logics
    crop_data = {
        "name": name,
        "quantity": quantity,
        "price": price,
        "farmer_id": farmer_id,
        "image_url": file_path,
        "status": "available"
    }

    result = crops.insert_one(crop_data)

    # Convert ObjectId to string
    crop_data["_id"] = str(result.inserted_id)

    return {
        "message": "Crop added successfully",
        "data": crop_data
    }


# -----------------------------
# 📈 Price Insights (Random Forest)
# -----------------------------
@router.post("/price-insights")
def price_insights(data: PriceInput):
    history = data.history

    if len(history) < 2:
        return {"error": "At least 2 price values required"}

    predicted = predict_price(history)

    if isinstance(predicted, dict):
        return predicted

    current_price = history[-1]

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