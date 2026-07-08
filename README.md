# LegiaCar Xiaozhi Server

Server trung gian cho Lia Assistant.

## Chức năng

- Nhận lệnh tiếng Việt từ Android qua HTTP `/command` hoặc WebSocket `/ws`
- Tự nhận dạng intent cơ bản:
  - YouTube search
  - Google Maps navigation
  - mở app
  - volume
  - media play/pause/next/previous
  - Racing/Home
- Nếu không hiểu lệnh, chuyển qua Gemini AI nếu đã có API key

## Chạy local

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Test:

```bash
curl -X POST http://localhost:8000/command \
  -H "Content-Type: application/json" \
  -d '{"text":"hey lia mở nhạc trẻ trên youtube"}'
```

Kết quả mẫu:

```json
{
  "success": true,
  "input": "hey lia mở nhạc trẻ trên youtube",
  "action": "youtube.search",
  "keyword": "nhac tre",
  "message": "Tìm nhac tre trên YouTube"
}
```

## Deploy Render

1. Tạo GitHub repository mới.
2. Upload toàn bộ file này lên repo.
3. Vào Render > New > Web Service.
4. Chọn repo.
5. Build Command:

```bash
pip install -r requirements.txt
```

6. Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

7. Thêm Environment Variable nếu dùng AI:

```bash
GEMINI_API_KEY=API_KEY_CUA_BAN
GEMINI_MODEL=gemini-1.5-flash
```

## URL Android dùng

HTTP:

```text
https://ten-server-render.onrender.com/command
```

WebSocket:

```text
wss://ten-server-render.onrender.com/ws
```
