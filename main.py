from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List

app = FastAPI()
security = HTTPBasic()

# MongoDB connection
client = MongoClient("mongodb+srv://Sayandas:Sayanat2001@cluster0.iu2x4ch.mongodb.net/")  
db = client["asset_performance_dashboard"]  

# Define Pydantic models
class Asset(BaseModel):
    asset_id: str
    asset_name: str
    asset_type: str
    location: str
    purchase_date: str
    initial_cost: float
    operational_status: str

class PerformanceMetric(BaseModel):
    asset_id: str
    uptime: int
    downtime: int
    maintenance_costs: float
    failure_rate: float
    efficiency: int

def is_asset_id_unique(asset_id: str):
    if db.assets.find_one({"asset_id": asset_id}):
        return False
    return True

def is_performance_metric_id_unique(asset_id: str):
    if db.performance_metrics.find_one({"asset_id": asset_id}):
        return False
    return True

def is_asset_id_valid(asset_id: str):
    return db.assets.find_one({"asset_id": asset_id}) is not None

def is_performance_metric_id_valid(asset_id: str):
    return db.performance_metrics.find_one({"asset_id": asset_id}) is not None

def get_current_username(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    if request.method != "GET":
        correct_username = "admin"
        correct_password = "password"
        if credentials.username != correct_username or credentials.password != correct_password:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return credentials.username
    return None

@app.get("/")
async def root():
    return {"message": "Welcome to the Asset Performance Dashboard API"}

# API endpoints for assets collection
@app.get("/assets/", response_model=List[Asset])
def get_assets(username: str = Depends(get_current_username)):
    assets = db.assets.find()  # Retrieve all assets from the MongoDB collection
    return list(assets)

@app.post("/assets/", response_model=Asset)
def create_asset(asset: Asset, username: str = Depends(get_current_username)):
    if not is_asset_id_unique(asset.asset_id):
        raise HTTPException(status_code=400, detail=f"Asset ID '{asset.asset_id}' already exists")
    asset_dict = asset.dict()
    result = db.assets.insert_one(asset_dict)  # Insert the new asset into the MongoDB collection
    return asset

@app.put("/assets/{asset_id}")
def update_asset(asset_id: str, updated_asset: Asset, username: str = Depends(get_current_username)):
    if not is_asset_id_valid(asset_id):
        raise HTTPException(status_code=404, detail="Asset not found")

    initial_asset = db.assets.find_one({"asset_id": asset_id})
    
    # Compare relevant fields of the updated asset with the initial asset
    if (updated_asset.asset_name == initial_asset['asset_name'] and
        updated_asset.asset_type == initial_asset['asset_type'] and
        updated_asset.location == initial_asset['location'] and
        updated_asset.purchase_date == initial_asset['purchase_date'] and
        updated_asset.initial_cost == initial_asset['initial_cost'] and
        updated_asset.operational_status == initial_asset['operational_status']):
        
        raise HTTPException(status_code=400, detail="Updated asset is identical to initial asset")
    
    # Update asset in the MongoDB collection based on asset_id
    updated_asset_data = updated_asset.dict(exclude_unset=True)  # Exclude unset fields from the updated data
    result = db.assets.update_one({"asset_id": asset_id}, {"$set": updated_asset_data})
    if result.modified_count == 1:
        return {"message": "Asset updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update asset")

@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: str, username: str = Depends(get_current_username)):
    # Delete asset from the MongoDB collection based on asset_id
    result = db.assets.delete_one({"asset_id": asset_id})
    if result.deleted_count == 1:
        return {"message": "Asset deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Asset not found")

# API endpoints for performance_metrics collection
@app.get("/performance_metrics/", response_model=List[PerformanceMetric])
def get_performance_metrics(username: str = Depends(get_current_username)):
    metrics = db.performance_metrics.find()  # Retrieve all performance metrics from the MongoDB collection
    return list(metrics)

@app.post("/performance_metrics/", response_model=PerformanceMetric)
def create_performance_metric(metric: PerformanceMetric, username: str = Depends(get_current_username)):
    if not is_performance_metric_id_unique(metric.asset_id):
        raise HTTPException(status_code=400, detail=f"Performance metric with ID '{metric.asset_id}' already exists")
    metric_dict = metric.dict()
    result = db.performance_metrics.insert_one(metric_dict)  # Insert the new performance metric into the MongoDB collection
    return metric

@app.put("/performance_metrics/{asset_id}")
def update_performance_metric(asset_id: str, updated_metric: PerformanceMetric, username: str = Depends(get_current_username)):
    if not is_performance_metric_id_valid(asset_id):
        raise HTTPException(status_code=404, detail="Performance metric not found")

    initial_metric = db.performance_metrics.find_one({"asset_id": asset_id})
    
    # Compare relevant fields of the updated metric with the initial metric
    if (updated_metric.uptime == initial_metric['uptime'] and
        updated_metric.downtime == initial_metric['downtime'] and
        updated_metric.maintenance_costs == initial_metric['maintenance_costs'] and
        updated_metric.failure_rate == initial_metric['failure_rate'] and
        updated_metric.efficiency == initial_metric['efficiency']):
        
        raise HTTPException(status_code=400, detail="Updated performance metric is identical to initial performance metric")
    
    # Update performance metric in the MongoDB collection based on asset_id
    updated_metric_data = updated_metric.dict(exclude_unset=True)  # Exclude unset fields from the updated data
    result = db.performance_metrics.update_one({"asset_id": asset_id}, {"$set": updated_metric_data})
    if result.modified_count == 1:
        return {"message": "Performance metric updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update performance metric")

@app.delete("/performance_metrics/{asset_id}")
def delete_performance_metric(asset_id: str, username: str = Depends(get_current_username)):
    # Delete performance metric from the MongoDB collection based on asset_id
    result = db.performance_metrics.delete_one({"asset_id": asset_id})
    if result.deleted_count == 1:
        return {"message": "Performance metric deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Performance metric not found")

# Additional endpoints for aggregating insights (protected with authentication)
@app.get("/insights/average_downtime")
def get_average_downtime(username: str = Depends(get_current_username)):
    pipeline = [
        {"$group": {"_id": None, "avg_downtime": {"$avg": "$downtime"}}}
    ]
    result = list(db.performance_metrics.aggregate(pipeline))
    return {"average_downtime": result[0]["avg_downtime"]} if result else {"message": "No data available for average downtime"}

@app.get("/insights/total_maintenance_costs")
def get_total_maintenance_costs(username: str = Depends(get_current_username)):
    pipeline = [
        {"$group": {"_id": None, "total_maintenance_costs": {"$sum": "$maintenance_costs"}}}
    ]
    result = list(db.performance_metrics.aggregate(pipeline))
    return {"total_maintenance_costs": result[0]["total_maintenance_costs"]} if result else {"message": "No data available for total maintenance costs"}

@app.get("/insights/high_failure_assets")
def get_high_failure_assets(username: str = Depends(get_current_username)):
    pipeline = [
    {"$match": {"failure_rate": {"$gt": 0.1}}},  # Example: Find assets with failure rates higher than 10%
    {"$project": {"asset_id": 1, "asset_name": 1, "failure_rate": 1, "_id": 0}}  # Exclude _id field from the response
    ]

    result = list(db.performance_metrics.aggregate(pipeline))
    return result if result else {"message": "No assets found with high failure rates"}
