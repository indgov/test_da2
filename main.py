# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TaxRequest(BaseModel):
    income: float

class TaxResponse(BaseModel):
    income: float
    state_tax: float
    total_tax: float

CALIFORNIA_STATE_TAX_RATE = 0.10  # Simplified tax rate for example purposes

def calculate_california_taxes(income: float) -> float:
    return income * CALIFORNIA_STATE_TAX_RATE

@app.post("/calculate_taxes/", response_model=TaxResponse)
def calculate_taxes(request: TaxRequest):
    if request.income < 0:
        raise HTTPException(status_code=400, detail="Income cannot be negative")
    
    state_tax = calculate_california_taxes(request.income)
    return TaxResponse(
        income=request.income,
        state_tax=state_tax,
        total_tax=request.income - state_tax
    )