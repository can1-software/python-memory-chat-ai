from fastapi import APIRouter, Depends

from app.config import AI_PROVIDER, GEMINI_API_KEY, GEMINI_MODEL
from app.dependencies import get_current_user
from app.models import User
from app.services import gemini_service

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/ai")
def debug_ai(current_user: User = Depends(get_current_user)):
    result = {
        "provider": AI_PROVIDER,
        "model": GEMINI_MODEL,
        "api_key_configured": bool(GEMINI_API_KEY),
    }

    try:
        response = gemini_service.generate_response(
            [{"role": "user", "content": "Sadece OK yaz."}]
        )
        result["status"] = "success"
        result["response"] = response
    except Exception as e:
        result["status"] = "error"
        result["error_type"] = type(e).__name__
        result["error_message"] = str(e)[:300]

    return result
