import os
import telebot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from dotenv import load_dotenv

# ======================================
# LOAD ENV
# ======================================

load_dotenv()

# ======================================
# TELEGRAM CONFIG
# ======================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# ======================================
# HOME PATHS
# ======================================

HOME_PATHS = {
    "🖥 Desktop": "C:/Users/Hp/Desktop",
    "⬇ Downloads": "C:/Users/Hp/Downloads",
    "📄 Documents": "C:/Users/Hp/Documents",
    "🖼 Pictures": "C:/Users/Hp/Pictures",
    "🎥 Videos": "C:/Users/Hp/Videos",
    "🎵 Music": "C:/Users/Hp/Music",
}

# ======================================
# HOME MENU
# ======================================

def send_home_menu(chat_id):

    keyboard = InlineKeyboardMarkup()

    # ==================================
    # HOME FOLDERS
    # ==================================

    for name, path in HOME_PATHS.items():

        if os.path.exists(path):

            keyboard.add(
                InlineKeyboardButton(
                    name,
                    callback_data=f"folder|{path}"
                )
            )

    # ==================================
    # DISK DRIVES
    # ==================================

    drives = ["C:\\", "D:\\", "E:\\", "F:\\"]

    for drive in drives:

        if os.path.exists(drive):

            keyboard.add(
                InlineKeyboardButton(
                    f"💽 Drive {drive}",
                    callback_data=f"drive_{drive[0]}"
                )
            )

    bot.send_message(
        chat_id,
        "🏠 Home Menu",
        reply_markup=keyboard
    )

# ======================================
# SEND FILE LIST
# ======================================

def send_file_list(chat_id, current_path):

    try:

        files = os.listdir(current_path)

        keyboard = InlineKeyboardMarkup()

        # ==================================
        # HOME BUTTON
        # ==================================

        keyboard.add(
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home"
            )
        )

        # ==================================
        # BACK BUTTON
        # ==================================

        parent = os.path.dirname(current_path)

        if current_path != parent:

            keyboard.add(
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data=f"folder|{parent}"
                )
            )

        # ==================================
        # SORT FILES
        # ==================================

        folders = []
        normal_files = []

        for file in files:

            full_path = os.path.join(
                current_path,
                file
            )

            if os.path.isdir(full_path):

                folders.append(file)

            else:

                normal_files.append(file)

        folders.sort()
        normal_files.sort()

        # ==================================
        # SHOW FOLDERS
        # ==================================

        for folder in folders:

            folder_path = os.path.join(
                current_path,
                folder
            )

            keyboard.add(
                InlineKeyboardButton(
                    f"📁 {folder}",
                    callback_data=f"folder|{folder_path}"
                )
            )

        # ==================================
        # SHOW FILES
        # ==================================

        for file in normal_files:

            file_path = os.path.join(
                current_path,
                file
            )

            keyboard.add(
                InlineKeyboardButton(
                    f"📄 {file}",
                    callback_data=f"file|{file_path}"
                )
            )

        bot.send_message(
            chat_id,
            f"📂 {current_path}",
            reply_markup=keyboard
        )

    except Exception as e:

        bot.send_message(
            chat_id,
            f"❌ Error: {e}"
        )

# ======================================
# MESSAGE HANDLER
# ======================================

@bot.message_handler(func=lambda msg: True)
def handle_message(message):

    print(message.text)

    text = message.text.lower()

    # ==================================
    # OPEN HOME
    # ==================================

    if "open home" in text:

        send_home_menu(
            message.chat.id
        )

    # ==================================
    # OPEN DESKTOP
    # ==================================

    elif "open desktop" in text:

        send_file_list(
            message.chat.id,
            os.path.expanduser("~/Desktop")
        )

    # ==================================
    # OPEN DOWNLOADS
    # ==================================

    elif "open downloads" in text:

        send_file_list(
            message.chat.id,
            os.path.expanduser("~/Downloads")
        )

    # ==================================
    # OPEN DOCUMENTS
    # ==================================

    elif "open documents" in text:

        send_file_list(
            message.chat.id,
            os.path.expanduser("~/Documents")
        )

# ======================================
# BUTTON HANDLER
# ======================================

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    try:

        # ==================================
        # HOME BUTTON
        # ==================================

        if call.data == "home":

            send_home_menu(
                call.message.chat.id
            )

            return

        # ==================================
        # DRIVE HANDLER
        # ==================================

        if call.data.startswith("drive_"):

            drive_letter = call.data.replace(
                "drive_",
                ""
            )

            drive_path = f"{drive_letter}:\\"

            send_file_list(
                call.message.chat.id,
                drive_path
            )

            return

        # ==================================
        # NORMAL ACTIONS
        # ==================================

        action, path = call.data.split("|", 1)

        # ==================================
        # OPEN FOLDER
        # ==================================

        if action == "folder":

            send_file_list(
                call.message.chat.id,
                path
            )

        # ==================================
        # DOWNLOAD FILE
        # ==================================

        elif action == "file":

            with open(path, "rb") as f:

                bot.send_document(
                    call.message.chat.id,
                    f
                )

    except Exception as e:

        bot.send_message(
            call.message.chat.id,
            f"❌ Error: {e}"
        )

# ======================================
# START BOT
# ======================================

print("🔥 Ultimate Telegram File Manager Started 🔥")

bot.infinity_polling()