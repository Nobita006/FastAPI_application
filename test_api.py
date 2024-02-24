import requests

# Set the base URL for your FastAPI application
base_url = "http://127.0.0.1:8000"

# Test user credentials
username = "admin"
password = "password"

# Authenticate with HTTP Basic Authentication
auth = requests.auth.HTTPBasicAuth(username, password)

# Define sample data for testing
sample_asset_data = {
    "asset_id": "A004",
    "asset_name": "Test Asset",
    "asset_type": "Test Type",
    "location": "Test Location",
    "purchase_date": "2022-02-23",
    "initial_cost": 10000.0,
    "operational_status": "Active"
}

sample_metric_data = {
    "asset_id": "A004",
    "uptime": 100,
    "downtime": 10,
    "maintenance_costs": 500.0,
    "failure_rate": 0.2,
    "efficiency": 90
}

# Test API endpoints

def test_get_assets():
    response = requests.get(f"{base_url}/assets/", auth=auth)
    print("GET /assets/")
    print(response.json())
    return response

def test_create_asset():
    response = requests.post(f"{base_url}/assets/", json=sample_asset_data, auth=auth)
    print("POST /assets/")
    print(response.json())
    return response

def test_update_asset():
    asset_id = sample_asset_data["asset_id"]
    update_asset_data = {
        "asset_id": asset_id,  # Include asset_id in the update data
        "asset_name": "Updated Asset Name",
        "asset_type": "Updated Asset Type",
        "location": "Updated Location",
        "purchase_date": "2022-02-23",
        "initial_cost": 12000.0,
        "operational_status": "Inactive"
    }
    response = requests.put(f"{base_url}/assets/{asset_id}", json=update_asset_data, auth=auth)
    print("PUT /assets/{asset_id}")
    print(response.json())
    return response

def test_delete_asset():
    asset_id = sample_asset_data["asset_id"]
    response = requests.delete(f"{base_url}/assets/{asset_id}", auth=auth)
    print("DELETE /assets/{asset_id}")
    print(response.json())
    return response

def test_get_performance_metrics():
    response = requests.get(f"{base_url}/performance_metrics/", auth=auth)
    print("GET /performance_metrics/")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to fetch performance metrics. Status code: {response.status_code}")
    return response

def test_create_performance_metric():
    response = requests.post(f"{base_url}/performance_metrics/", json=sample_metric_data, auth=auth)
    print("POST /performance_metrics/")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to create performance metric. Status code: {response.status_code}")
    return response

def test_update_performance_metric():
    metric_id = sample_metric_data["asset_id"]
    update_metric_data = {
        "asset_id": metric_id,  # Include asset_id in the update data
        "uptime": 120,
        "downtime": 15,
        "maintenance_costs": 600.0,
        "failure_rate": 0.3,
        "efficiency": 85
    }
    response = requests.put(f"{base_url}/performance_metrics/{metric_id}", json=update_metric_data, auth=auth)
    print("PUT /performance_metrics/{asset_id}")
    print(response.json())
    return response

def test_delete_performance_metric():
    metric_id = sample_metric_data["asset_id"]
    response = requests.delete(f"{base_url}/performance_metrics/{metric_id}", auth=auth)
    print("DELETE /performance_metrics/{asset_id}")
    print(response.json())
    return response

def test_get_average_downtime():
    response = requests.get(f"{base_url}/insights/average_downtime", auth=auth)
    print("GET /insights/average_downtime")
    print(response.json())
    return response

def test_get_total_maintenance_costs():
    response = requests.get(f"{base_url}/insights/total_maintenance_costs", auth=auth)
    print("GET /insights/total_maintenance_costs")
    print(response.json())
    return response

def test_get_high_failure_assets():
    response = requests.get(f"{base_url}/insights/high_failure_assets", auth=auth)
    print("GET /insights/high_failure_assets")
    print(response.json())
    return response

# Run individual tests
if __name__ == "__main__":
    test_get_assets()
    test_create_asset()
    test_update_asset()
    test_delete_asset()
    test_get_performance_metrics()
    test_create_performance_metric()
    test_update_performance_metric()
    test_delete_performance_metric()
    test_get_average_downtime()
    test_get_total_maintenance_costs()
    test_get_high_failure_assets()
