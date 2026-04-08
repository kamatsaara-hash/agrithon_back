from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Routers
from routers.farmer import router as farmer_router
from routers.buyer import router as buyer_router
from routers.delivery import router as delivery_router
from routers.alerts import router as alerts_router
from routers.auth_routes import router as auth_router

# Initialize app
app = FastAPI(title="Smart Agri Supply Chain")

# -----------------------------
# 📦 Static Files (for images)
# -----------------------------
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# -----------------------------
# 🔗 Include Routers
# -----------------------------
app.include_router(farmer_router, prefix="/farmer", tags=["Farmer"])
app.include_router(buyer_router, prefix="/buyer", tags=["Buyer"])
app.include_router(delivery_router, prefix="/delivery", tags=["Delivery"])
app.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# -----------------------------
# 🏠 Home Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "Agri Backend Running 🚀"}