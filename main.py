from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from uuid import uuid4
import re
import math

app = FastAPI()

# In-memory storage for receipts
receipts_store = {}

# Schemas
class Item(BaseModel):
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$", example="Mountain Dew 12PK")
    price: str = Field(..., pattern=r"^\d+\.\d{2}$", example="6.49")

class Receipt(BaseModel):
    retailer: str = Field(..., pattern=r"^[\w\s\-&]+$", example="M&M Corner Market")
    purchaseDate: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", example="2022-01-01")
    purchaseTime: str = Field(..., pattern=r"^\d{2}:\d{2}$", example="13:01")
    items: list[Item] = Field(..., min_items=1)
    total: str = Field(..., pattern=r"^\d+\.\d{2}$", example="6.49")

class ReceiptResponse(BaseModel):
    id: str = Field(..., pattern=r"^\S+$", example="adb6b560-0eef-42bc-9d16-df48f30e89b2")

class PointsResponse(BaseModel):
    points: int = Field(..., example=100)

# Endpoints
@app.post("/receipts/process", response_model=ReceiptResponse)
def process_receipt(receipt: Receipt):
    receipt_id = str(uuid4())
    points = calculate_points(receipt)
    receipts_store[receipt_id] = points
    return {"id": receipt_id}

@app.get("/receipts/{id}/points", response_model=PointsResponse)
def get_points(id: str = Path(..., pattern=r"^\S+$")):
    points = receipts_store.get(id)
    if points is None:
        raise HTTPException(status_code=404, detail="No receipt founf for that id")
    return {"points": points}

# Point calculation logic
def calculate_points(receipt: Receipt):
    points = 0
    points += sum(c.isalnum() for c in receipt.retailer)  # Retailer name
    #print("points retailer name", points)
    total = float(receipt.total)
    if total.is_integer():
        points += 50
    #print("points after total round", points)
    if total % 0.25 == 0:
        points += 25
    #print("points after checking mitilple 0.25", points)
    points += (len(receipt.items) // 2) * 5  # Items
    #print("points after total number of items", points)
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            #print("Short description", item.shortDescription)
            #print("price after multiplying with 0.2",float(item.price) * 0.2)
            #print("price after multiplying with 0.2 and adding 0.5",(float(item.price) * 0.2) + 0.5)
            points += int(math.ceil((float(item.price) * 0.2) + 0.5))  # Item description
            #print("points after added for the item description ", points)
    #print("points after multiple of 3 and round", points)
    day = int(receipt.purchaseDate.split("-")[2])
    
    if day % 2 == 1:
        points += 6
    #print("points after date is odd", points)
    hour = int(receipt.purchaseTime.split(":")[0])
    if 14 <= hour < 16:
        points += 10
    #print("points after purchase time b/w 2 and 4", points)
    return points

if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(app, host="127.0.0.1", port=8000)