"""
Engine for generating a screenplay script from episode beats.
"""

from app.models.story_models import EpisodeStructure, SeriesBible
from app.utils.gemini_client import call_llm

class ScriptGenerator:
    """
    Engine to convert structured episode beats into a formatted screenplay.
    """

    async def generate_script(self, episode: EpisodeStructure, series_bible: SeriesBible, is_last_episode: bool = False, previous_ending: str = "") -> str:
        """
        Asynchronously generates a screenplay script based on the episode structure.
        """
        beats_text = "\n".join(
            [f"- {beat.content}" for beat in episode.beats]
        )

        if is_last_episode:
            ending_instruction = (
                f"This is the FINAL episode. ALL storylines MUST be fully resolved.\n"
                f"The central conflict '{series_bible.central_conflict}' must reach a definitive conclusion.\n"
                f"End with FADE OUT. — absolutely no cliffhangers, no SMASH CUT TO BLACK.\n"
                f"The final moment must feel emotionally complete and earned.\n"
            )
        else:
            ending_instruction = (
                f"End on a hard cliffhanger naturally "
                f"(a door slams, someone appears, a message arrives) — "
                f"it should feel earned not announced.\n"
                f"End with SMASH CUT TO BLACK.\n"
            )

        ending_context = ""
        if previous_ending:
            ending_context = (
                f"CRITICAL — The previous episode ended with this scene:\n"
                f"{previous_ending}\n"
                f"Your FADE IN must directly continue from that moment.\n\n"
            )
            
        prompt = (
            f"You are an award-winning screenplay writer for short-form vertical video.\n\n"
            f"{ending_context}"
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
            f"6. {ending_instruction}\n"
            f"7. 250-350 words total — this is 90 seconds of video\n"
        )
        
        if is_last_episode:
            prompt += f"8. FINAL EPISODE ONLY — end with FADE OUT. Using SMASH CUT TO BLACK is strictly forbidden.\n"

        prompt += f"\nWrite only the screenplay. No commentary. No labels.\n"

        script_text = await call_llm(prompt)
        script_text = script_text.strip()

        if script_text.startswith("```"):
            lines = script_text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            script_text = "\n".join(lines).strip()

        return script_text