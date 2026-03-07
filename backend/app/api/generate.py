"""
API router for generation operations.
"""
from fastapi import APIRouter
from typing import Dict, Any

from app.models.story_models import StoryIdea, RegenerateRequest
from app.engines.pipeline_engine import PipelineEngine

router = APIRouter()
pipeline_engine = PipelineEngine()
bible_generator = pipeline_engine.bible_generator

@router.post("/generate-series")
async def generate_series_endpoint(story: StoryIdea) -> Dict[str, Any]:
    """
    Endpoint to trigger the full end-to-end AI story generation pipeline asynchronously in parallel.
    
    Args:
        story: The initial StoryIdea with title, description, and genre.
        
    """
    return await pipeline_engine.run_pipeline(story)

@router.post("/regenerate-episode")
async def regenerate_episode_endpoint(request: RegenerateRequest) -> Dict[str, Any]:
    return await pipeline_engine.regenerate_episode(
        episode_number=request.episode_number,
        series_bible=request.series_bible,
        suggestions=request.suggestions,
        is_last_episode=request.is_last_episode,
        prior_context=request.prior_context,
        previous_ending=request.previous_ending,
        next_episode_hook=request.next_episode_hook
    )

@router.post("/suggest-episodes")
async def suggest_episodes_endpoint(story: StoryIdea) -> Dict[str, Any]:
    """
    Endpoint to suggest an episode count based on the basic story details.
    
    Args:
        story: The initial StoryIdea with title, description, and genre.
        
    Returns:
        A dictionary containing the suggested_count.
    """
    count = await bible_generator.suggest_episode_count(story)
    return {"suggested_count": count}
