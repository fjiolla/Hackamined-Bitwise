"""
Engine for generating a screenplay script from episode beats.
"""

from app.models.story_models import EpisodeStructure, SeriesBible
from app.utils.groq_client import call_llm

class ScriptGenerator:
    """
    Engine to convert structured episode beats into a formatted screenplay.
    """

    def generate_script(self, episode: EpisodeStructure, series_bible: SeriesBible) -> str:
        """
        Generates a screenplay script based on the episode structure.

        Args:
            episode: The structured episode containing the narrative beats.
            series_bible: The foundational elements of the series.

        Returns:
            A string formatted as a screenplay.
        """
        # Format the beats to include in the prompt
        beats_text = "\n".join(
            [f"- {beat.content}" for beat in episode.beats]
        )

        prompt = (
            f"You are an award-winning screenplay writer for short-form vertical video.\n\n"
            f"Series Context:\n"
            f"Protagonist: {series_bible.protagonist}\n"
            f"Supporting Characters: {', '.join(series_bible.supporting_characters)}\n"
            f"Central Conflict: {series_bible.central_conflict}\n\n"
            f"Write Episode {episode.episode_number} as a complete screenplay using "
            f"these story points as your guide:\n"
            f"{beats_text}\n\n"
            f"STRICT RULES:\n"
            f"1. Start with FADE IN:\n"
            f"2. Use proper format: INT./EXT. LOCATION - TIME, action lines, "
            f"character names above dialogue\n"
            f"3. NEVER write Hook, Conflict, Escalation, Twist, or Cliffhanger anywhere\n"
            f"4. Flow naturally from scene to scene with no labels\n"
            f"5. Dialogue must be punchy — under 10 words per line\n"
            f"6. End on a hard cliffhanger naturally "
            f"(a door slams, someone appears, a message arrives) — "
            f"it should feel earned not announced\n"
            f"7. End with SMASH CUT TO BLACK\n"
            f"8. 250-350 words total — this is 90 seconds of video\n\n"
            f"Write only the screenplay. No commentary. No labels.\n"
        )

        script_text = call_llm(prompt).strip()
        
        # Clean up any generic markdown wrapping if Gemini still provides it
        if script_text.startswith("```"):
            lines = script_text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            script_text = "\n".join(lines).strip()

        return script_text
