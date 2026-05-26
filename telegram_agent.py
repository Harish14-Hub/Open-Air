import time
import requests
from playwright.sync_api import sync_playwright

# ==========================================
# TELEGRAM CONFIG
# ==========================================

BOT_TOKEN = "8729670895:AAEoUK39d4VG_hyhpWiIprt-RZs3smsi16w"
CHAT_ID = "7404337836"

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

last_update_id = 0

# ==========================================
# CLEAR OLD TELEGRAM MESSAGES
# ==========================================

try:

    response = requests.get(
        f"{BASE_URL}/getUpdates"
    ).json()

    updates = response.get("result", [])

    if updates:

        last_update_id = updates[-1]["update_id"]

        print("🧹 Old messages cleared")

except Exception as e:

    print("⚠ Error clearing old updates:", e)

# ==========================================
# PLAYWRIGHT START
# ==========================================

playwright = sync_playwright().start()

browser = playwright.chromium.launch(
    headless=False,
    args=["--disable-dev-shm-usage"]
)

page = browser.new_page()

page.set_default_timeout(30000)

print("🔥 Telegram AI Agent Started 🔥")

# ==========================================
# MAIN LOOP
# ==========================================

while True:

    try:

        # ==================================
        # GET ONLY NEW TELEGRAM MESSAGES
        # ==================================

        response = requests.get(
            f"{BASE_URL}/getUpdates",
            params={
                "offset": last_update_id + 1
            }
        ).json()

        updates = response.get("result", [])

        for update in updates:

            last_update_id = update["update_id"]

            message = update.get("message")

            if not message:
                continue

            text = message.get(
                "text",
                ""
            ).lower()

            print(f"\n📩 New Task: {text}")

            # ==================================
            # RESET PREVIOUS TASK
            # ==================================

            page.goto("about:blank")

            page.wait_for_timeout(1000)

            # ==================================
            # OPEN YOUTUBE
            # ==================================

            if "open youtube" in text:

                page.goto(
                    "https://youtube.com"
                )

                print("✅ YouTube Opened")

                requests.get(
                    f"{BASE_URL}/sendMessage",
                    params={
                        "chat_id": CHAT_ID,
                        "text": "✅ YouTube Opened"
                    }
                )

            # ==================================
            # PLAY SONG / VIDEO
            # ==================================

            elif "play" in text:

                search_query = (
                    text
                    .replace(
                        "open youtube and play",
                        ""
                    )
                    .replace(
                        "play",
                        ""
                    )
                    .replace(
                        "song",
                        ""
                    )
                    .strip()
                )

                page.goto(
                    "https://youtube.com"
                )

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

                requests.get(
                    f"{BASE_URL}/sendMessage",
                    params={
                        "chat_id": CHAT_ID,
                        "text": f"▶ Playing: {search_query}"
                    }
                )

            # ==================================
            # OPEN LINKEDIN
            # ==================================

            elif "linkedin" in text:

                page.goto(
                    "https://linkedin.com"
                )

                print("💼 LinkedIn Opened")

                requests.get(
                    f"{BASE_URL}/sendMessage",
                    params={
                        "chat_id": CHAT_ID,
                        "text": "💼 LinkedIn Opened"
                    }
                )

            # ==================================
            # WEATHER / QUESTIONS / SEARCH
            # ==================================

            elif (
                "weather" in text
                or "climate" in text
                or "temperature" in text
                or "what" in text
                or "who" in text
                or "search" in text
            ):

                query = (
                    text
                    .replace("search", "")
                    .strip()
                )

                print(f"🔍 Searching: {query}")

                page.goto(
                    f"https://www.google.com/search?q={query}"
                )

                page.wait_for_timeout(4000)

                # ==================================
                # WEATHER EXTRACTION
                # ==================================

                try:

                    temp_element = page.locator(
                        "#wob_tm"
                    ).first

                    location_element = page.locator(
                        "#wob_loc"
                    ).first

                    condition_element = page.locator(
                        "#wob_dc"
                    ).first

                    if temp_element.count() > 0:

                        temp = temp_element.inner_text()

                        location = (
                            location_element.inner_text()
                        )

                        condition = (
                            condition_element.inner_text()
                        )

                        answer = (
                            f"🌤 Weather in {location}\n"
                            f"🌡 Temperature: {temp}°C\n"
                            f"☁ Condition: {condition}"
                        )

                    # ==================================
                    # NORMAL SEARCH RESULT
                    # ==================================

                    else:

                        first_heading = page.locator(
                            "h3"
                        ).first

                        if first_heading.count() > 0:

                            answer = (
                                first_heading.inner_text()
                            )

                        else:

                            answer = (
                                "❌ No answer found"
                            )

                except Exception as e:

                    answer = (
                        "❌ Could not fetch weather"
                    )

                print("🤖 Answer:", answer)

                requests.get(
                    f"{BASE_URL}/sendMessage",
                    params={
                        "chat_id": CHAT_ID,
                        "text": answer
                    }
                )

            # ==================================
            # EXIT AI AGENT
            # ==================================

            elif "exit" in text:

                requests.get(
                    f"{BASE_URL}/sendMessage",
                    params={
                        "chat_id": CHAT_ID,
                        "text": "👋 AI Agent Stopped"
                    }
                )

                print("👋 Exiting Agent")

                browser.close()

                playwright.stop()

                exit()

            # ==================================
            # UNKNOWN COMMAND
            # ==================================

            else:

                print("❌ Unknown Command")

                requests.get(
                    f"{BASE_URL}/sendMessage",
                    params={
                        "chat_id": CHAT_ID,
                        "text": "❌ Unknown Command"
                    }
                )

        time.sleep(2)

    except Exception as e:

        print("⚠ Error:", e)

        time.sleep(5)