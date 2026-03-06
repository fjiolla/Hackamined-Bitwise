"""
Engine for generating sequence of structured episodes based on a SeriesBible.
"""

import json
import asyncio
from typing import Dict, Any, List

from app.models.story_models import SeriesBible, EpisodeBeat, EpisodeStructure
from app.utils.gemini_client import call_llm


class EpisodeGenerator:
    """
    Engine to generate a sequence of structured episodes for vertical storytelling.
    """

    async def generate_episode(self, episode_number: int, series_bible: SeriesBible, prior_context: str = "") -> EpisodeStructure:
        """
        Generates a structured episode based on the SeriesBible.

        Args:
            episode_number: The episode number to generate.
            series_bible: The foundational elements of the series.

        Returns:
            An EpisodeStructure object containing the structured 90-second episode beats.
        """
        # 1 Build prompt using series_bible
        prompt = (
            f"Generate Episode {episode_number} beats based on the series bible.\n"
            f"Return ONLY valid JSON with no extra text or markdown codeblocks or explanation.\n"
            f"The JSON should contain precisely these string keys: 'hook', 'conflict', 'escalation', 'twist', 'cliffhanger'.\n"
            f"Each value should be a short string describing the beat.\n"
            f"Archetype: {series_bible.archetype}\n"
            f"Protagonist: {series_bible.protagonist}\n"
            f"Supporting Characters: {', '.join(series_bible.supporting_characters)}\n"
            f"Central Conflict: {series_bible.central_conflict}\n"
        )

        if prior_context:
            last_cliffhanger = prior_context.split("cliffhanger:")[-1].split("\n")[0].strip() if "cliffhanger:" in prior_context else ""
            prompt += (
                f"\nCRITICAL CONTINUITY RULES:\n"
                f"1. Previous episodes context:\n{prior_context}\n"
                f"2. The hook beat (0-15s) MUST show the direct aftermath of this cliffhanger: {last_cliffhanger}\n"
                f"3. Do NOT start a new storyline or ignore what happened previously.\n"
                f"4. Characters, relationships and tension from prior episodes must carry forward.\n"
            )

        # 2 Call placeholder function
        response_text = await call_llm(prompt)
        response_text = response_text.strip()
        
        # Parse the structured JSON output
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()
            
        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError:
            response_data = {
                "hook": "Error generating hook",
                "conflict": "Error generating conflict",
                "escalation": "Error generating escalation",
                "twist": "Error generating twist",
                "cliffhanger": "Error generating cliffhanger"
            }

        # 3 Expect LLM to return beat descriptions
        # 4 Convert beats into EpisodeBeat objects
        beats = [
            EpisodeBeat(
                beat_type="Hook",
                content=response_data.get("hook", ""),
                time_range="0-15s"
            ),
            EpisodeBeat(
                beat_type="Conflict",
                content=response_data.get("conflict", ""),
                time_range="15-35s"
            ),
            EpisodeBeat(
                beat_type="Escalation",
                content=response_data.get("escalation", ""),
                time_range="35-55s"
            ),
            EpisodeBeat(
                beat_type="Twist",
                content=response_data.get("twist", ""),
                time_range="55-75s"
            ),
            EpisodeBeat(
                beat_type="Cliffhanger",
                content=response_data.get("cliffhanger", ""),
                time_range="75-90s"
            )
        ]

        # 5 Return EpisodeStructure
        return EpisodeStructure(
            episode_number=episode_number,
            beats=beats
        )

    async def generate_series(self, series_bible: SeriesBible, episode_count: int = 5) -> List[EpisodeStructure]:
        """
        Generates a sequence of structured episodes mapping the whole series.

        Args:
            series_bible: The foundational elements of the series.
            episode_count: The total number of episodes in the series. Default is 5.

        Returns:
            A list of EpisodeStructure objects representing the generated series.
        """
        episodes = []
        prior_context = ""
        for i in range(1, episode_count + 1):
            episode = await self.generate_episode(
                episode_number=i,
                series_bible=series_bible,
                prior_context=prior_context
            )
            episodes.append(episode)
            # Build context summary for next episode
            cliffhanger_beat = episode.beats[-1].content
            beat_summary = " | ".join([f"{b.beat_type}: {b.content}" for b in episode.beats])
            if i < episode_count:
                prior_context += (
                    f"Episode {i} full summary: {beat_summary}\n"
                    f"Episode {i} ended on this cliffhanger: {cliffhanger_beat}\n"
                    f"Episode {i+1} MUST open by directly resolving or continuing from that cliffhanger.\n\n"
                )
            else:
                prior_context += f"Episode {i} full summary: {beat_summary}\n"

        return episodes

    async def regenerate_episode(
        self,
        episode_number: int,
        series_bible: SeriesBible,
        suggestions: List[str],
        is_last_episode: bool = False,
        prior_context: str = "",
        next_episode_hook: str = ""
    ) -> EpisodeStructure:

        suggestions_text = "\n".join([f"- {s}" for s in suggestions])

        prompt = (
            f"Regenerate Episode {episode_number} beats based on the series bible.\n"
            f"Return ONLY valid JSON with no extra text.\n"
            f"The JSON must contain exactly these keys: 'hook', 'conflict', 'escalation', 'twist', 'cliffhanger'.\n"
            f"Each value should be a detailed narrative description of that beat.\n\n"
            f"Archetype: {series_bible.archetype}\n"
            f"Protagonist: {series_bible.protagonist}\n"
            f"Supporting Characters: {', '.join(series_bible.supporting_characters)}\n"
            f"Central Conflict: {series_bible.central_conflict}\n\n"
            f"CRITICAL — The previous version of this episode had these weaknesses.\n"
            f"You MUST directly fix each one in your regenerated version:\n"
            f"{suggestions_text}\n"
        )


        if prior_context:
            last_cliffhanger = prior_context.split("cliffhanger:")[-1].split("\n")[0].strip() if "cliffhanger:" in prior_context else ""
            prompt += (
                f"\nCRITICAL CONTINUITY:\n"
                f"1. Previous episodes context:\n{prior_context}\n"
                f"2. Hook beat MUST directly continue from: {last_cliffhanger}\n"
                f"3. Do NOT ignore prior events or start a new storyline.\n"
            )
        if next_episode_hook:
            prompt += (
                f"\nIMPORTANT — The next episode opens with: {next_episode_hook}\n"
                f"Your cliffhanger MUST naturally lead into that.\n"
            )
            
        response_text = await call_llm(prompt)
        response_text = response_text.strip()

        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()

        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError:
            response_data = {
                "hook": "Error regenerating hook",
                "conflict": "Error regenerating conflict",
                "escalation": "Error regenerating escalation",
                "twist": "Error regenerating twist",
                "cliffhanger": "Error regenerating cliffhanger"
            }

        beats = [
            EpisodeBeat(beat_type="Hook", content=response_data.get("hook", ""), time_range="0-15s"),
            EpisodeBeat(beat_type="Conflict", content=response_data.get("conflict", ""), time_range="15-35s"),
            EpisodeBeat(beat_type="Escalation", content=response_data.get("escalation", ""), time_range="35-55s"),
            EpisodeBeat(beat_type="Twist", content=response_data.get("twist", ""), time_range="55-75s"),
            EpisodeBeat(beat_type="Cliffhanger", content=response_data.get("cliffhanger", ""), time_range="75-90s")
        ]

        return EpisodeStructure(episode_number=episode_number, beats=beats, is_last_episode=is_last_episode)
