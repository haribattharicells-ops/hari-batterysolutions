# =======================================================
# FINAL - HARI BATTERY SOLUTION - GEMINI MAIN + CHATGPT BACKUP
# PRIVACY 100% SAFE - PRIVATE CHANNEL ONLY
# =======================================================
import telebot, google.generativeai as genai, os
from openai import OpenAI
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
PRIVATE_CHANNEL_ID = int(os.environ.get("PRIVATE_CHANNEL_ID"))

genai.configure(api_key=GEMINI_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")
openai_client = OpenAI(api_key=OPENAI_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

MOOLAI = """You are HARI BATTERY SOLUTION EXPERT BOT. 
You are from Hari Battery Solution shop.
You help customers with Inverter, Battery, UPS, Solar queries.
Explain battery backup, service, price, warranty in simple way.
Reply in user's language Tamil/English/Hindi. 
Friendly shop owner style. Always helpful for battery solution."""

def send_to_private(user, q, ans, ai_name):
    try:
        log = f"🔒 HARI BATTERY LOG [{ai_name}]\n👤 {user}\n💬 Q: {q}\n🤖 A: {ans[:500]}...\n⏰ {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        bot.send_message(PRIVATE_CHANNEL_ID, log)
    except: pass

def get_ai_answer(question):
    try:
        r = gemini_model.generate_content(f"{MOOLAI}\n\nQ: {question}")
        return r.text, "Gemini"
    except:
        try:
            r = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": MOOLAI},{"role": "user", "content": question}]
            )
            return r.choices[0].message.content, "ChatGPT-Backup"
        except Exception as e:
            return f"தடங்கல் தலைவரே: {e}", "Error"

@bot.message_handler(commands=['start'])
def welcome(m): bot.reply_to(m, "🔋 வணக்கம் தலைவரே! HARI BATTERY SOLUTION-க்கு வாங்க! Inverter, Battery, UPS எது வேணும்னாலும் கேளுங்க! நான் ரெடி!")

@bot.message_handler(content_types=['text','photo','voice','audio'])
def main_handler(m):
    try:
        user_info = f"{m.from_user.first_name} (@{m.from_user.username})"
        q = m.text if m.content_type == 'text' else f"{m.content_type}"
        if m.content_type == 'text' and m.text.startswith('/'): return
        ans, ai_name = get_ai_answer(q)
        bot.reply_to(m, ans)
        send_to_private(user_info, q, ans, ai_name)
    except Exception as e: bot.reply_to(m, f"Error: {e}")

print("HARI BATTERY BOT READY - GEMINI + CHATGPT BACKUP - PRIVATE SAFE!")
bot.infinity_polling()
