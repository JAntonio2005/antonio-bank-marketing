# app.py  (para Bank Marketing con 'deposit' como target)
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from joblib import load
import pandas as pd

origins = ["*"]

app = FastAPI(title="Bank Marketing – Subscription Prediction")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

MODEL_PATH = Path(__file__).resolve().parent / "model" / "bank-marketing-rf-v1.joblib"
model = load(MODEL_PATH)  # pipeline (pre + modelo)

# IMPORTANTE: estos campos son TODAS las columnas de bank.csv menos 'deposit'
class InputData(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    default: str
    balance: int
    housing: str
    loan: str
    contact: str
    day: int
    month: str
    duration: int
    campaign: int
    pdays: int
    previous: int
    poutcome: str

class OutputData(BaseModel):
    score: float  # prob de 'yes'

@app.get("/")
def root():
    return {"status": "ok", "model_file": MODEL_PATH.name}

@app.post("/score", response_model=OutputData)
def score(data: InputData):
    df = pd.DataFrame([data.dict()])
    proba_yes = float(model.predict_proba(df)[0, 1])
    return {"score": proba_yes}
