import json
import random
import uuid
from datetime import datetime, timedelta

# Helper functions
def random_timestamp():
    base_time = datetime.now()
    return (base_time - timedelta(days=random.randint(0, 365))).isoformat()

def generate_auth():
    return {
        "type": "Bearer",
        "token": str(uuid.uuid4()),
        "expires_in": 3600
    }

def generate_pagination():
    return {
        "page": random.randint(1, 10),
        "page_size": 25,
        "total_pages": 10,
        "total_items": 250
    }

def generate_error_handling():
    return {
        "error_code": "ERR_" + str(random.randint(1000, 9999)),
        "message": "An unexpected error occurred",
        "details": {
            "field": "name",
            "issue": "Must not be empty"
        }
    }

def generate_complex_api(index):
    resource = random.choice(["users", "orders", "payments", "products"])
    method = random.choice(["GET", "POST", "PUT", "DELETE"])
    endpoint = f"/api/v2/{resource}/{index if method != 'POST' else ''}".rstrip("/")
    
    api = {
        "id": index,
        "endpoint": endpoint,
        "method": method,
        "auth": generate_auth(),
        "description": f"Complex {method} API for {resource}",
        "parameters": {
            "query": {
                "search": "test",
                "sort_by": "date",
                "page": 1,
                "limit": 25
            },
            "headers": {
                "Authorization": "Bearer <token>",
                "X-Request-ID": str(uuid.uuid4())
            },
            "body": {
                "id": str(uuid.uuid4()),
                "name": f"{resource.capitalize()}Name{index}",
                "amount": round(random.uniform(10.0, 500.0), 2),
                "timestamp": random_timestamp(),
                "metadata": {
                    "source": "web",
                    "campaign": "spring_sale"
                }
            } if method in ["POST", "PUT"] else None
        },
        "response": {
            "status": 200 if method != "DELETE" else 204,
            "pagination": generate_pagination() if method == "GET" else None,
            "data": {
                "id": index,
                "message": f"{method} operation completed on {resource} #{index}"
            },
            "errors": generate_error_handling() if random.random() > 0.8 else None
        },
        "webhook": {
            "trigger_event": f"{resource}_updated",
            "callback_url": f"https://webhooks.example.com/{resource}/{index}/callback",
            "payload": {
                "event": "update",
                "resource_id": index,
                "timestamp": random_timestamp()
            }
        }
    }

    return api

# Generate 160 complex APIs
complex_apis = [generate_complex_api(i) for i in range(1, 161)]

# Save to JSON file
output_path = "complex_Sample_apis_160.json"
with open(output_path, "w") as f:
    json.dump(complex_apis, f, indent=4)

print(f"160 complex APIs saved to {output_path}")
