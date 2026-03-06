from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

CLIFFHANGER_ARCHETYPES = [
    "character faces immediate life threatening danger",
    "shocking secret is suddenly revealed",
    "protagonist discovers everything they believed was a lie",
    "mysterious stranger appears with unknown intentions",
    "countdown to catastrophic irreversible event"
]

ENGAGING_DESCRIPTIONS = [
    "intense dramatic scene with high stakes",
    "unexpected twist that changes everything",
    "emotional confrontation between characters",
    "mystery deepens with new revelation",
    "urgent action with time pressure"
]

BORING_DESCRIPTIONS = [
    "characters casually talking with no tension",
    "slow scene with no conflict or stakes",
    "routine activity with no drama",
    "lengthy explanation with no action",
    "uneventful transition between scenes"
]

SECRET_ARCHETYPES = [
    "character reveals hidden truth or secret",
    "shocking discovery changes everything",
    "hidden information finally comes to light"
]

THREAD_ARCHETYPES = [
    "unresolved mystery left open",
    "unanswered question hanging in the air",
    "loose end that needs resolution"
]

def semantic_similarity(text: str, archetypes: list) -> list:
    text_emb = model.encode(text, convert_to_tensor=True)
    archetype_embs = model.encode(archetypes, convert_to_tensor=True)
    similarities = util.cos_sim(text_emb, archetype_embs)[0]
    return [float(s) for s in similarities]

def score_cliffhanger_semantic(text: str) -> dict:
    scores = semantic_similarity(text, CLIFFHANGER_ARCHETYPES)
    
    def scale(s):
        if s >= 0.4: return 2
        elif s >= 0.25: return 1
        else: return 0
        
    breakdown = {
        "unresolved_tension": scale(scores[0]),
        "revelation_hook": scale(scores[1]),
        "stakes_escalation": scale(scores[2]),
        "character_jeopardy": scale(scores[3]),
        "time_pressure": scale(scores[4])
    }
    return {
        "score": sum(breakdown.values()),
        "breakdown": breakdown
    }

def score_engagement(text: str) -> float:
    text_emb = model.encode(text, convert_to_tensor=True)
    engaging_embs = model.encode(ENGAGING_DESCRIPTIONS, convert_to_tensor=True)
    boring_embs = model.encode(BORING_DESCRIPTIONS, convert_to_tensor=True)
    engaging = float(util.cos_sim(text_emb, engaging_embs).mean())
    boring = float(util.cos_sim(text_emb, boring_embs).mean())
    return engaging - boring

def score_narrative_flow(beats: list) -> list:
    contents = [b.content for b in beats]
    embeddings = model.encode(contents, convert_to_tensor=True)
    issues = []
    for i in range(len(embeddings) - 1):
        similarity = float(util.cos_sim(embeddings[i], embeddings[i+1]))
        if similarity > 0.85:
            issues.append({
                "type": "narrative_stagnation",
                "beat_index": i + 1,
                "message": f"Beat {i+1} to {i+2} shows no narrative progression"
            })
        if similarity < 0.15:
            issues.append({
                "type": "narrative_disconnect",
                "beat_index": i + 1,
                "message": f"Beat {i+1} to {i+2} has jarring tonal disconnect"
            })
    return issues

def is_secret_revealed(text: str) -> bool:
    scores = semantic_similarity(text, SECRET_ARCHETYPES)
    return max(scores) > 0.4

def is_unresolved_thread(text: str) -> bool:
    scores = semantic_similarity(text, THREAD_ARCHETYPES)
    return max(scores) > 0.4
