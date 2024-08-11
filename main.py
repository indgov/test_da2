from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class TaxInput(BaseModel):
    income: float
    filing_status: Optional[str] = "single"

# Simplified California tax brackets for demonstration
# This is not accurate for real tax calculation
TAX_RATES = {
    'single': [
        (0, 8809, 0.01),
        (8810, 20883, 0.02),
        # Add more brackets as needed
    ],
    'married': [
        # Brackets for married filing jointly
    ]
}

def calculate_tax(income: float, status: str):
    brackets = TAX_RATES.get(status.lower(), TAX_RATES['single'])
    tax = 0
    remaining_income = income
    
    for lower, upper, rate in brackets:
        if income <= lower:
            continue
        taxable = min(remaining_income, upper - lower + 1) if upper else remaining_income
        tax += taxable * rate
        remaining_income -= taxable
        if remaining_income <= 0:
            break
    
    return round(tax, 2)

@app.post("/calculate_tax/")
async def tax_calculation(item: TaxInput):
    if item.income < 0:
        raise HTTPException(status_code=400, detail="Income cannot be negative")
    tax = calculate_tax(item.income, item.filing_status)
    return {"tax": tax, "income": item.income}
