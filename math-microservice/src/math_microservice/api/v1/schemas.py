# src/math_microservice/api/v1/schemas.py
from pydantic import BaseModel, Field

class PowerRequest(BaseModel):
    base: float = Field(..., description="Base number")
    exponent: float = Field(..., description="Exponent number")

class FibonacciRequest(BaseModel):
    n: int = Field(..., ge=0, le=1000, description="Index of Fibonacci sequence")

class FactorialRequest(BaseModel):
    n: int = Field(..., ge=0, le=1000, description="Number to compute factorial for")
