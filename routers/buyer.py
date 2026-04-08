from fastapi import APIRouter
from database import crops, db
from bson import ObjectId

router = APIRouter()

# -----------------------------
# 🛒 Browse Available Crops
# -----------------------------
@router.get("/browse")
def browse():
    data = []
    for doc in crops.find({"status": "available"}):
        doc["_id"] = str(doc["_id"])  # ✅ FIX
        data.append(doc)
    return data


# -----------------------------
# 📦 Place Order
# -----------------------------
@router.post("/order")
def place_order(data: dict):

    try:
        crop_id = ObjectId(data["crop_id"])
    except:
        return {"error": "Invalid crop_id"}

    crop = crops.find_one({"_id": crop_id})

    if not crop:
        return {"error": "Crop not found"}

    if crop["status"] != "available":
        return {"error": "Crop not available"}

    if data["quantity"] > crop["quantity"]:
        return {"error": "Not enough quantity"}

    total_price = crop["price"] * data["quantity"]

    order = {
        "crop_id": str(crop_id),  # ✅ convert
        "farmer_id": crop["farmer_id"],
        "buyer_id": data["buyer_id"],
        "quantity": data["quantity"],
        "total_price": total_price,
        "status": "pending"
    }

    result = db.orders.insert_one(order)

    # ✅ add string id
    order["_id"] = str(result.inserted_id)

    # update quantity
    crops.update_one(
        {"_id": crop_id},
        {"$inc": {"quantity": -data["quantity"]}}
    )

    return {
        "message": "Order placed successfully",
        "order": order
    }