from fastapi import APIRouter
from database import db
from bson import ObjectId
from pydantic import BaseModel

router = APIRouter()

# -----------------------------
# 🚚 Get Available Deliveries
# -----------------------------
@router.get("/available")
def available_orders():
    data = []
    for doc in db.orders.find({"status": "pending"}):
        doc["_id"] = str(doc["_id"])  # ✅ IMPORTANT
        data.append(doc)
    return data


class DeliveryInput(BaseModel):
    order_id: str
    driver_id: str


@router.post("/accept")
def accept_delivery(data: DeliveryInput):

    try:
        obj_id = ObjectId(data.order_id)
    except:
        return {"error": "Invalid order_id"}

    order = db.orders.find_one({"_id": obj_id})

    if not order:
        return {"error": "Order not found"}

    db.orders.update_one(
        {"_id": obj_id},
        {"$set": {
            "status": "shipped",
            "delivery_id": data.driver_id
        }}
    )

    return {
        "message": "Delivery assigned successfully",
        "order_id": data.order_id,
        "driver_id": data.driver_id
    }

# -----------------------------
# 📊 (Optional) Driver Deliveries
# -----------------------------
@router.get("/my-deliveries/{driver_id}")
def my_deliveries(driver_id: str):
    return list(
        db.orders.find(
            {"delivery_id": driver_id},
            {"_id": 0}
        )
    )