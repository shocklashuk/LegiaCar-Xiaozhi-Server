import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from intent_parser import parse_intent
from gemini_engine import ask_gemini

app = FastAPI(title="LegiaCar Xiaozhi Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    text: str
    device_id: str | None = None
    app_version: str | None = None


@app.get("/")
def root():
    return {
        "success": True,
        "service": "LegiaCar Xiaozhi Server",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"success": True, "status": "ok"}


@app.post("/command")
async def command(req: TextRequest):
    text = (req.text or "").strip()
    if not text:
        return {
            "success": False,
            "action": "none",
            "message": "Không có nội dung lệnh"
        }

    result = parse_intent(text)

    if result.get("action") == "ai.chat":
        answer = await ask_gemini(text)
        result["answer"] = answer
        result["message"] = answer

    return {
        "success": True,
        "input": text,
        **result
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({
        "success": True,
        "type": "connected",
        "message": "Lia đã kết nối Xiaozhi Server"
    })

    try:
        while True:
            data = await websocket.receive_json()
            text = str(data.get("text", "")).strip()

            if not text:
                await websocket.send_json({
                    "success": False,
                    "action": "none",
                    "message": "Không có nội dung lệnh"
                })
                continue

            result = parse_intent(text)

            if result.get("action") == "ai.chat":
                answer = await ask_gemini(text)
                result["answer"] = answer
                result["message"] = answer

            await websocket.send_json({
                "success": True,
                "input": text,
                **result
            })

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.close(code=1011, reason=str(e))
