import requests

def uber_fetch_jobs():
    url = "https://www.uber.com/api/loadSearchJobsResults"
    data = {
        "limit": 10000,
        "page": 0,
    }
    headers = {
        "x-csrf-token": "x",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json() if response.status_code == 200 else None
