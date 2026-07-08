from app.config import AI_PROVIDER
from app.services import gemini_service


class AIServiceError(Exception):
    pass


def _get_last_user_message(messages: list[dict]) -> str:
    for message in reversed(messages):
        if message["role"] == "user":
            return message["content"]
    return ""


def _generate_mock_response(messages: list[dict]) -> str:
    user_message = _get_last_user_message(messages)
    return f"Bu bir test AI cevabıdır. Mesajını aldım: {user_message}"


def _generate_gemini_response(messages: list[dict]) -> str:
    try:
        return gemini_service.generate_response(messages)
    except Exception as e:
        print("AI PROVIDER ERROR:", repr(e))
        raise AIServiceError("Gemini request failed.") from e


def generate_ai_response(messages: list[dict]) -> str:
    if AI_PROVIDER == "mock":
        return _generate_mock_response(messages)

    if AI_PROVIDER == "gemini":
        return _generate_gemini_response(messages)

    print("AI PROVIDER ERROR:", f"Unsupported AI_PROVIDER: {AI_PROVIDER}")
    raise AIServiceError(f"Unsupported AI_PROVIDER: {AI_PROVIDER}")
