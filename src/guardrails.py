# guardrails.py

BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "api key",
    "password",
    "secret",
    "token"
]


def validate_question(question):

    question = question.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in question:
            return False

    return True