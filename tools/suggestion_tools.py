from typing import List
import random

STUDY_SUGGESTIONS = [
    "Try the Pomodoro technique: 25 minutes focused study, 5 minutes break.",
    "Review your notes within 24 hours for better retention.",
    "Use spaced repetition for memorizing key concepts.",
    "Teach someone else what you've learned to reinforce understanding.",
    "Create mind maps to visualize connections between topics.",
    "Take regular breaks to maintain focus and prevent burnout.",
    "Practice active recall instead of passive reading.",
    "Use multiple learning resources for different perspectives."
]

def suggest_topic() -> str:
    suggestion = random.choice(STUDY_SUGGESTIONS)
    return f"Here's a study tip: {suggestion}"

SUGGESTION_TOOL = {
    "type": "function",
    "function": {
        "name": "suggest_topic",
        "description": "Provide a random study suggestion or tip. Use this when the user asks for study advice or suggestions.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}
