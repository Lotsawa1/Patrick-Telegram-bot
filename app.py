# Patrick — Telegram bot for English practice (Render-ready version)

import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import openai

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Greetings and options
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first = update.effective_user.first_name
    reply_keyboard = [["Переклад", "Обговорити новини", "Подискутивати"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(f"Привіт, {user_first}! 👋\n\nЩо робимо сьогодні?", reply_markup=markup)

# Main logic: reply with OpenAI
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    # Compose context prompt for OpenAI
    messages = [
        {"role": "system", "content": "Patrick — доброзичливий асистент, створений Костею для практики англійської мови.\n\n🔸 Спілкуйся українською, звертайся до студента на 'ти'. Будь уважним, підтримуй, жартуй делікатно.\n🔸 Якщо студент робить помилку: запропонуй знайти її самостійно (👀), покажи де помилка (➡️), правильний варіант (✅), пояснення (📚).\n🔸 Якщо студент уникає використання нових слів — мʼяко підказуй, як вставити.\n🔹 Кожне заняття починається з 'Що робимо сьогодні?' і трьома варіантами.\n🔸 У форматах Переклад, Обговорити новини, Подискутивати — дотримуйся спеціальної логіки, пояснень, виправлень.\n🔁 У всіх форматах використовується лексика групи студента (зберігається окремо).\n📌 Завжди підтримуй діалог.\n📚 Коли студент не розуміє слово — поясни українською з прикладом.\n⛔ Не давай переклад одразу.\n🎯 Ціль — підтримати мислення і стимулювати природну розмову.\n"},
        {"role": "user", "content": user_input},
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        reply_text = response.choices[0].message["content"]
        await update.message.reply_text(reply_text)
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        await update.message.reply_text("Вибач, сталася помилка. Спробуй ще раз трохи пізніше 🙏")

# Token and run
if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    application.run_polling()
