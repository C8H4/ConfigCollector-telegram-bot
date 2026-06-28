import os
import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "your BOT TOKEN"
OWNER_ID = OWNER number id

SUB_LINKS = [
    "https://raw.githubusercontent.com/ThomasJasperthecat/sub/main/sublist1.txt",
    "https://raw.githubusercontent.com/masir-sefid/Sub/main/@Masir_Sefid.txt",
    "https://sub.iampedi5.live/sub/base64.txt",
    "https://sub.whitedns.one/sub/mihomo.yaml",
    "http://main.pythash.tr/FRkh99yBGCllN/01736620-2086-4c0b-a86e-52ebfe64dd12/#pythash",
    "https://raw.githubusercontent.com/masir-sefid/Sub/main/Telegram-Channel-@Masir_Sefid.txt",
    "https://c6et83fe1u99lr8j5w4s9iwik9565bqx.pages.dev/sub/fragment/g4lWgI*%40zehfoOEK?app=xray#%F0%9F%92%A6%20BPB%20Fragment",
]

bot = telebot.TeleBot(BOT_TOKEN)

def owner_only(func):
    def wrapper(message):
        if message.from_user.id != OWNER_ID:
            bot.reply_to(message, "Access Denied")
            return
        func(message)
    return wrapper

def main_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, persistent=True)
    kb.add(KeyboardButton("🔄 Get Fresh Configs"))
    return kb

def fetch_configs():
    lines = []
    for url in SUB_LINKS:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                for line in r.text.splitlines():
                    line = line.strip()
                    if line:
                        lines.append(line)
        except Exception:
            pass
    return "\n".join(lines)

@bot.message_handler(commands=["start"])
@owner_only
def start(message):
    bot.send_message(message.chat.id, "Ready.", reply_markup=main_kb())

@bot.message_handler(func=lambda m: m.text == "🔄 Get Fresh Configs")
@owner_only
def get_configs(message):
    bot.send_chat_action(message.chat.id, "typing")
    configs = fetch_configs()
    if not configs:
        bot.reply_to(message, "No configs fetched.")
        return
    if len(configs) > 4000:
        path = "configs.txt"
        with open(path, "w") as f:
            f.write(configs)
        with open(path, "rb") as f:
            bot.send_document(message.chat.id, f, visible_file_name="configs.txt")
        os.remove(path)
    else:
        bot.send_message(message.chat.id, f"```\n{configs}\n```", parse_mode="Markdown")

bot.infinity_polling()
