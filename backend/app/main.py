"""
Main FastAPI application module for EpisodeIQ.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Added import

from .api import generate, analyse

app = FastAPI(
    title="EpisodeIQ API",
    description="Backend skeleton for EpisodeIQ",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Include routers from the api subpackage
app.include_router(generate.router, prefix="/api/generate", tags=["Generate"])
app.include_router(analyse.router, prefix="/api/analyse", tags=["Analyse"])

@app.get("/")
async def root():
    """
    Health check and root endpoint.
    """
    return {"status": "ok", "message": "Welcome to the EpisodeIQ API"}