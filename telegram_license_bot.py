import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Import the license generation function
from generate_license import generate_license

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", 0))

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def check_auth(update: Update) -> bool:
    """Checks if the user sending the message is the admin."""
    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Unauthorized. You do not have permission to use this bot.")
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update):
        return
    await update.message.reply_text(
        "Welcome to the License Generator Bot!\n\n"
        "Usage: /gen <HWID> <DAYS>\n"
        "Example: /gen ABCDEF12 30"
    )

async def gen_license(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update):
        return

    # context.args is a list of arguments passed to the command
    args = context.args
    if not args or len(args) < 1:
        await update.message.reply_text("Usage: /gen <HWID> [<DAYS>]\nExample: /gen ABCDEF12 30")
        return

    hwid = args[0]
    
    # Default to 30 days if not provided
    days = 30
    if len(args) > 1:
        try:
            days = int(args[1])
        except ValueError:
            await update.message.reply_text("Invalid number of days. Using default 30 days.")

    try:
        expiry = datetime.now() + timedelta(days=days)
        license_key = generate_license(hwid, expiry)
        
        message = (
            f"✅ *License Generated*\n\n"
            f"*HWID:* `{hwid}`\n"
            f"*Expiry Date:* {expiry.strftime('%Y-%m-%d')} ({days} days)\n\n"
            f"*License Key:*\n`{license_key}`"
        )
        await update.message.reply_text(message, parse_mode="Markdown")
        await update.message.reply_text(f"`{license_key}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Error generating license: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", gen_license))

    print("Bot is running...")
    app.run_polling()
