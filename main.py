from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from intent_parser import parse_intent

app = FastAPI(
    title="LegiaCar Xiaozhi Server",
    version="1.0.0"
)


class CommandRequest(BaseModel):
    text: str



@app.get("/")
def home():

    return {
        "success": True,
        "service": "LegiaCar Xiaozhi Server",
        "status": "running",
        "version": "1.0.0"
    }



@app.post("/command")
def command(
    data: CommandRequest
):

    result = parse_intent(
        data.text
    )

    return {
        "success": True,
        "input": data.text,
        **result
    }



@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    print(
        "Xiaozhi WebSocket connected"
    )


    try:

        while True:

            data = await websocket.receive_json()

            text = data.get(
                "text",
                ""
            )


            result = parse_intent(
                text
            )


            await websocket.send_json({

                "success": True,

                "input": text,

                **result

            })


    except WebSocketDisconnect:

        print(
            "Xiaozhi WebSocket disconnected"
        )
