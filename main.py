import requests
from playwright.sync_api import sync_playwright

# =====================================
# AI COMMAND CLASSIFIER
# =====================================

def ask_ai(task):

    prompt = f"""
You are an AI command classifier.

Understand the user request and return commands.

Allowed Commands:

OPEN_YOUTUBE
PLAY_YOUTUBE
OPEN_GOOGLE
GOOGLE_SEARCH
OPEN_LINKEDIN
SEARCH_AI_JOBS
EXIT

Rules:
- Return only commands
- No explanation
- No markdown
- Commands can be combined

Examples:
open youtube
-> OPEN_YOUTUBE

play thriller song
-> PLAY_YOUTUBE

open youtube and play thriller
-> OPEN_YOUTUBE PLAY_YOUTUBE

search python jobs
-> GOOGLE_SEARCH

User Request:
{task}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data.get("response", "").strip()


# =====================================
# MAIN AI AGENT
# =====================================

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    print("🔥 Harish AI Agent Started 🔥")

    while True:

        try:

            task = input("\nAsk AI: ")

            task_lower = task.lower()

            ai_result = ask_ai(task)

            print("AI Command:", ai_result)

            # =====================================
            # OPEN YOUTUBE
            # =====================================

            if "OPEN_YOUTUBE" in ai_result:

                page.goto("https://youtube.com")

                print("✅ YouTube Opened")

            # =====================================
            # PLAY YOUTUBE VIDEO / SONG
            # =====================================

            if "PLAY_YOUTUBE" in ai_result:

                search_query = (
                    task_lower
                    .replace("open youtube and play", "")
                    .replace("play", "")
                    .replace("song", "")
                    .strip()
                )

                page.goto("https://youtube.com")

                page.wait_for_timeout(3000)

                page.fill(
                    "input[name='search_query']",
                    search_query
                )

                page.keyboard.press("Enter")

                page.wait_for_timeout(3000)

                first_video = page.locator(
                    "ytd-video-renderer a#video-title"
                ).first

                first_video.click()

                print(f"▶ Playing: {search_query}")

            # =====================================
            # OPEN GOOGLE
            # =====================================

            if "OPEN_GOOGLE" in ai_result:

                page.goto("https://google.com")

                print("✅ Google Opened")

            # =====================================
            # GOOGLE SEARCH
            # =====================================

            if "GOOGLE_SEARCH" in ai_result:

                search_query = (
                    task_lower
                    .replace("search", "")
                    .strip()
                )

                page.goto("https://google.com")

                page.wait_for_timeout(2000)

                page.fill(
                    "textarea",
                    search_query
                )

                page.keyboard.press("Enter")

                print(f"🔍 Searching: {search_query}")

            # =====================================
            # OPEN LINKEDIN
            # =====================================

            if "OPEN_LINKEDIN" in ai_result:

                page.goto("https://linkedin.com")

                print("✅ LinkedIn Opened")

            # =====================================
            # SEARCH AI JOBS
            # =====================================

            if "SEARCH_AI_JOBS" in ai_result:

                page.goto(
                    "https://www.google.com/search?q=AI+jobs"
                )

                print("💼 Searching AI Jobs")

            # =====================================
            # EXIT
            # =====================================

            if "EXIT" in ai_result:

                print("👋 Exiting AI Agent")
                break

        except Exception as e:

            print("⚠ Error:", e)

    browser.close()