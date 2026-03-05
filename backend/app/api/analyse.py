"""
API router for analysis operations.
"""
from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def analyse_endpoint():
    """
    Placeholder endpoint for analysing content.
    """
    return {"message": "Analyse endpoint placeholder"}
