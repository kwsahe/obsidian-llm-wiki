import os
from datetime import datetime

VAULT_PATH = r"C:\Users\sangh\Desktop\Code\Obsidian\obsidian-llm-wiki"
CALENDAR_PATH = os.path.join(VAULT_PATH, "02-calendar")

def create_daily_note():
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    day_str = today.strftime("%A")
    filename = f"{date_str}.md"
    filepath = os.path.join(CALENDAR_PATH, filename)

    if os.path.exists(filepath):
        print(f"이미 존재: {filename}")
        return

    content = f"""---
created: {date_str}
day: {day_str}
tags: [daily]
mood:
focus:
---

# {date_str} ({day_str})

## 오늘 할 일
- [ ]
- [ ]
- [ ]

## 공부/개발 기록

## 에러 & 해결

## 취준 활동

## 내일 할 일
- [ ]
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"생성 완료: {filename}")

if __name__ == "__main__":
    create_daily_note()
