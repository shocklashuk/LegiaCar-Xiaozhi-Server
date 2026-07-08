    # YouTube play / search

    if "youtube" in cmd or "ytb" in cmd or "you tube" in cmd:

        keyword = extract_after(cmd, [
            "mo youtube tim",
            "mo youtube",
            "tim youtube",
            "youtube",
            "ytb",
            "you tube"
        ])

        keyword = keyword.replace("tren", "").strip()


        if not keyword:
            keyword = extract_after(
                cmd,
                [
                    "mo",
                    "phat",
                    "nghe",
                    "tim"
                ]
            )


        # Có yêu cầu mở/phát/nghe -> tự play
        if contains_any(
            cmd,
            [
                "mo",
                "phat",
                "nghe",
                "chay",
                "bat"
            ]
        ):

            if keyword:
                return {
                    "action": "youtube.play",
                    "keyword": keyword,
                    "message": f"Phát {keyword} trên YouTube"
                }


        # Chỉ tìm kiếm
        if keyword:
            return {
                "action": "youtube.search",
                "keyword": keyword,
                "message": f"Tìm {keyword} trên YouTube"
            }


        return {
            "action": "youtube.open",
            "message": "Mở YouTube"
        }
