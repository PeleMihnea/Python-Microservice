# src/math_microservice/api/v1/endpoints.py
from fastapi import APIRouter, HTTPException
from .schemas import PowerRequest, FibonacciRequest, FactorialRequest
from math_microservice.services.math_ops import (
    compute_power,
    compute_fibonacci,
    compute_factorial,
)

router = APIRouter()

@router.post("/power", response_model=dict)
async def power(req: PowerRequest):
    try:
        result = compute_power(req.base, req.exponent)
        return {"result": result}
    except OverflowError:
        raise HTTPException(400, "Result too large")

@router.post("/fibonacci", response_model=dict)
async def fibonacci(req: FibonacciRequest):
    return {"result": compute_fibonacci(req.n)}

@router.post("/factorial", response_model=dict)
async def factorial(req: FactorialRequest):
    return {"result": compute_factorial(req.n)}
