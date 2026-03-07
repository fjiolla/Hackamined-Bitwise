"""
Pydantic data models for the storytelling system.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class RegenerateRequest(BaseModel):
    episode_number: int
    series_bible: 'SeriesBible'
    suggestions: List[str]
    is_last_episode: bool = False
    prior_context: str = ""
    previous_ending: str = ""
    next_episode_hook: str = ""


class StoryIdea(BaseModel):
    """
    Model representing a basic story idea.
    """
    title: str
    description: str
    genre: str
    episode_count: int = Field(default=5, ge=5, le=8)


class SeriesBible(BaseModel):
    """
    Model representing the foundational elements and lore of a series.
    """
    archetype: str
    protagonist: str
    supporting_characters: List[str]
    central_conflict: str


class EpisodeBeat(BaseModel):
    """
    Model representing a specific narrative beat within an episode.
    """
    beat_type: str
    content: str
    time_range: str


class EpisodeStructure(BaseModel):
    """
    Model representing the structural breakdown of a single episode.
    """
    episode_number: int
    beats: List[EpisodeBeat]
    script: str = ""
    is_last_episode: bool = False
