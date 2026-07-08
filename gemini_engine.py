import os
import httpx

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


async def ask_gemini(text: str) -> str:
    if not GEMINI_API_KEY:
        return "Lia chưa được cấu hình Gemini API key trên server."

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "Bạn là Lia, trợ lý tiếng Việt trong xe Legia Car. "
                            "Trả lời ngắn, dễ nghe, phù hợp khi người dùng đang lái xe.\n\n"
                            f"Người dùng nói: {text}"
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 180
        }
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.post(url, json=payload)
            res.raise_for_status()
            data = res.json()

        candidates = data.get("candidates", [])
        if not candidates:
            return "Lia chưa nhận được câu trả lời từ AI."

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            return "Lia chưa có nội dung trả lời."

        return parts[0].get("text", "Lia chưa có nội dung trả lời.").strip()

    except Exception as e:
        return f"Lia gặp lỗi khi gọi AI: {e}"
