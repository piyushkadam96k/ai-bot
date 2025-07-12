# Simple Telegram Echo Bot
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import google.genai as genai
import concurrent.futures

# Set your Gemini API key (set GEMINI_API_KEY or GOOGLE_API_KEY as env var, or pass here)
client = genai.Client(api_key="GEMINI_API_KEY")

def gemini_chat(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini error: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user_message = update.message.text
        try:
            loop = asyncio.get_running_loop()
            with concurrent.futures.ThreadPoolExecutor() as pool:
                reply = await loop.run_in_executor(pool, gemini_chat, user_message)
        except Exception as e:
            reply = f"Error: {e}"
        await update.message.reply_text(reply or "No response from Gemini.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Hello! I am a Gemini-powered chatbot created by piyush_kadam. 🤖\n"
            "Commands:\n"
            "/start - Show this message\n"
            "/help - Get help\n"
            "/social - My social media profiles\n"
            "\nSend me any message and I'll respond!"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message: 
        await update.message.reply_text(
            "Send any message and I'll reply using Gemini AI.\n"
            "Use /start to see the welcome message."
        )

async def social_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        keyboard = [
            [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/piyush_kadam96k?igsh=MXZlY3J1a3ZuOHNj")],
            [InlineKeyboardButton("🐦 Twitter", url="https://x.com/KadamAmol395841?t=mxTjO8Tk5qkgDorhVxP1Fw&s=09")],
            [InlineKeyboardButton("💻 GitHub", url="https://github.com/piyushkadam96k")],
            [InlineKeyboardButton("👥 study material", url="https://t.me/piyush_kadam96k")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🌐 My Social Media Profiles:",
            reply_markup=reply_markup
        )

def main():
    app = ApplicationBuilder().token("BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("social", social_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
