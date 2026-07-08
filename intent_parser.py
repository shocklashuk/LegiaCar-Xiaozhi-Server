import re
import unicodedata


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def contains_any(text: str, words: list[str]) -> bool:
    return any(w in text for w in words)


def remove_prefixes(text: str) -> str:
    prefixes = [
        "hey lia", "lia oi", "lia", "le gia", "legia", "xiaozhi", "tieu tri",
        "ban oi", "tro ly oi"
    ]
    result = text
    for p in prefixes:
        if result.startswith(p + " "):
            result = result[len(p):].strip()
        elif result == p:
            result = ""
    return result


def extract_after(text: str, keys: list[str]) -> str:
    for key in keys:
        idx = text.find(key)
        if idx >= 0:
            return text[idx + len(key):].strip()
    return ""


def parse_intent(raw_text: str) -> dict:
    text = normalize(raw_text)
    cmd = remove_prefixes(text)

    if not cmd:
        return {
            "action": "wake",
            "message": "Lia đang nghe"
        }

    # HOME / Racing
    if contains_any(cmd, ["ve man hinh chinh", "mo man hinh chinh", "home"]):
        return {"action": "app.home", "message": "Về màn hình chính"}

    if contains_any(cmd, ["racing", "che do racing", "mo racing", "dua xe"]):
        return {"action": "app.racing", "message": "Mở Racing Mode"}

    # Media
    if contains_any(cmd, ["tam dung", "pause", "dung nhac", "dung video"]):
        return {"action": "media.pause", "message": "Tạm dừng"}

    if contains_any(cmd, ["phat tiep", "play", "phat nhac", "tiep tuc phat"]):
        return {"action": "media.play", "message": "Phát tiếp"}

    if contains_any(cmd, ["bai tiep", "next", "chuyen bai", "video tiep"]):
        return {"action": "media.next", "message": "Chuyển bài tiếp theo"}

    if contains_any(cmd, ["bai truoc", "previous", "prev", "quay lai bai"]):
        return {"action": "media.previous", "message": "Quay lại bài trước"}

    # Volume
    percent_match = re.search(r"(am luong|volume|tieng).*?(\d{1,3})", cmd)
    if percent_match:
        value = max(0, min(100, int(percent_match.group(2))))
        return {
            "action": "volume.set",
            "value": value,
            "message": f"Đặt âm lượng {value}%"
        }

    if contains_any(cmd, ["tang am luong", "tang tieng", "to hon", "lon hon", "volume up"]):
        return {"action": "volume.up", "step": 10, "message": "Tăng âm lượng"}

    if contains_any(cmd, ["giam am luong", "giam tieng", "nho hon", "volume down"]):
        return {"action": "volume.down", "step": 10, "message": "Giảm âm lượng"}

    if contains_any(cmd, ["tat tieng", "mute", "im lang"]):
        return {"action": "volume.mute", "message": "Tắt tiếng"}

    # Maps navigation
    if contains_any(cmd, ["dan duong", "chi duong", "di den", "toi", "tim duong"]):
        place = extract_after(cmd, ["dan duong den", "chi duong den", "tim duong den", "di den", "toi"])
        if place:
            return {
                "action": "maps.navigate",
                "place": place,
                "message": f"Dẫn đường đến {place}"
            }

    # YouTube search
    if "youtube" in cmd or "ytb" in cmd or "you tube" in cmd:
        keyword = extract_after(cmd, [
            "mo youtube tim", "mo youtube", "tim youtube", "youtube", "ytb", "you tube"
        ])
        keyword = keyword.replace("tren", "").strip()
        if not keyword:
            keyword = extract_after(cmd, ["mo", "phat", "tim"])

        if keyword:
            return {
                "action": "youtube.search",
                "keyword": keyword,
                "message": f"Tìm {keyword} trên YouTube"
            }
        return {"action": "youtube.open", "message": "Mở YouTube"}

    # Google search
    if contains_any(cmd, ["tim google", "tim tren google", "google"]):
        keyword = extract_after(cmd, ["tim tren google", "tim google", "google", "tim"])
        if keyword:
            return {
                "action": "google.search",
                "keyword": keyword,
                "message": f"Tìm {keyword} trên Google"
            }
        return {"action": "google.open", "message": "Mở Google"}

    # Open apps
    app_patterns = {
        "maps": ["mo ban do", "mo google map", "mo maps", "ban do"],
        "youtube": ["mo youtube", "mo ytb"],
        "camera": ["mo camera", "mo cam", "camera"],
        "zalo": ["mo zalo", "zalo"],
        "vietmap": ["mo vietmap", "vietmap"]
    }

    for app_name, keys in app_patterns.items():
        if contains_any(cmd, keys):
            return {
                "action": "app.open",
                "app": app_name,
                "message": f"Mở {app_name}"
            }

    # AI fallback
    return {
        "action": "ai.chat",
        "message": "Lia đang xử lý bằng AI"
    }
