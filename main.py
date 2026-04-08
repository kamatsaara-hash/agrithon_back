from fastapi import FastAPI
from routers.farmer import router as farmer_router
from routers.buyer import router as buyer_router
from routers.delivery import router as delivery_router
from routers.alerts import router as alerts_router 

app = FastAPI(title="Smart Agri Supply Chain")

app.include_router(farmer_router, prefix="/farmer")
app.include_router(buyer_router, prefix="/buyer")
app.include_router(delivery_router, prefix="/delivery")
app.include_router(alerts_router, prefix="/alerts")

@app.get("/")
def home():
    return {"message": "Agri Backend Running"}