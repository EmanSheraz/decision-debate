import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  

client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"


PERSONAS = {
    "FOR": (
        "You are 'The Optimist' in a live debate. Argue FOR the user's decision. "
        "Be persuasive, concrete, and a little punchy. 3-4 sentences max. "
        "If there is a prior AGAINST argument, directly rebut its strongest point "
        "before making your own."
    ),
    "AGAINST": (
        "You are 'The Skeptic' in a live debate. Argue AGAINST the user's decision. "
        "Be sharp, specific, and a little punchy. 3-4 sentences max. "
        "Directly rebut the strongest point the FOR side just made before making "
        "your own case."
    ),
}

JUDGE_SYSTEM = (
    "You are 'The Judge'. You just watched a debate between an Optimist and a "
    "Skeptic about the user's decision. Give a short, balanced verdict: what's "
    "the strongest argument on each side, and one concrete piece of advice. "
    "5-6 sentences max. Do not just restate both sides — actually take a stance "
    "on what matters most for THIS decision."
)


def _format_transcript(transcript: list[dict]) -> str:
    if not transcript:
        return "(debate has not started yet)"
    return "\n\n".join(f"{t['speaker']}: {t['text']}" for t in transcript)


def generate_turn(speaker: str, decision: str, transcript: list[dict]) -> str:
    system = PERSONAS[speaker]
    user_msg = (
        f"The user's decision to debate: \"{decision}\"\n\n"
        f"Debate so far:\n{_format_transcript(transcript)}\n\n"
        f"Now give your next turn as {speaker}."
    )
    resp = client.chat.completions.create(
        model=MODEL,
        max_tokens=300,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
    )
    return (resp.choices[0].message.content or "").strip()
def generate_verdict(decision: str, transcript: list[dict]) -> str:
    user_msg = (
        f"The user's decision: \"{decision}\"\n\n"
        f"Full debate:\n{_format_transcript(transcript)}\n\n"
        f"Give your verdict."
    )
    resp = client.chat.completions.create(
        model=MODEL,
        max_tokens=400,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": user_msg},
        ],
    )
    return (resp.choices[0].message.content or "").strip()

def run_debate(decision: str, rounds: int = 3) -> dict:
    transcript = []
    for _ in range(rounds):
        for speaker in ("FOR", "AGAINST"):
            text = generate_turn(speaker, decision, transcript)
            transcript.append({"speaker": speaker, "text": text})
    verdict = generate_verdict(decision, transcript)
    return {"transcript": transcript, "verdict": verdict}