# client.py
import requests

body = {
    "age": 39,
    "job": "technician",
    "marital": "single",
    "education": "secondary",
    "default": "no",
    "balance": 1500,
    "housing": "yes",
    "loan": "no",
    "contact": "cellular",
    "day": 5,
    "month": "may",
    "duration": 180,
    "campaign": 1,
    "pdays": 999,      # 999 suele significar "no contactado anteriormente"
    "previous": 0,
    "poutcome": "unknown"
}

resp = requests.post("http://127.0.0.1:8000/score", json=body, timeout=10)
print(resp.json())
