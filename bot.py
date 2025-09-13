import telebot
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = '1984772645:AAGoojVfYCHRJN5sTHo4IKwLjUp1-03SjyY'
MINI_APP_URL = 'https://splendorous-dodol-424be3.netlify.app/templates/'
BOT_NAME = "RentalBot"
VERSION = "1.0.0"
ADMIN_USER_ID = 1485409432  # User ID to receive notifications

bot = telebot.TeleBot(BOT_TOKEN)

# Create main menu keyboard
def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🏠 Open Rentals"))
    keyboard.add(KeyboardButton("ℹ️ Help"), KeyboardButton("📄 About"))
    return keyboard

# Create inline keyboard for mini app
def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup()
    web_app = telebot.types.WebAppInfo(MINI_APP_URL)
    keyboard.add(InlineKeyboardButton('Open Rentals App', web_app=web_app))
    return keyboard

# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name or "User"
    username = message.from_user.username or "No username"
    user_id = message.from_user.id
    welcome_message = (
        f"👋 Welcome {user_name} to {BOT_NAME}!\n"
        "Your one-stop solution for rental ads.\n"
        "Use the menu below to get started:"
    )
    bot.reply_to(message, welcome_message, reply_markup=get_main_menu())
    bot.send_message(
        message.chat.id, 
        "Click below to open the rentals app:\n بزرگ ترین آرشیو اطلاعات اجاره ملک ایرانیان در سراسر دنیا",
        reply_markup=get_inline_keyboard()
    )
    
    # Send notification to admin
    try:
        bot.send_message(
            ADMIN_USER_ID,
            f"New user started the bot:\nUsername: @{username}\nUser ID: {user_id}"
        )
        logger.info(f"Sent notification to admin about new user: @{username}")
    except Exception as e:
        logger.error(f"Failed to send notification to admin: {str(e)}")

# Help command handler
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "📚 *Help Menu*\n\n"
        "Available commands:\n"
        "/start - Start the bot and show main menu\n"
        "/help - Show this help message\n"
        "/about - About the bot\n\n"
        "Features:\n"
        "🏠 View and post rental ads\n"
        "📱 Access our web app for full functionality\n"
        "📞 Contact support: @VlanSupport"
    )
    bot.reply_to(message, help_text, parse_mode='Markdown')

# About command handler
@bot.message_handler(commands=['about'])
def about_command(message):
    about_text = (
        f"ℹ️ *About {BOT_NAME}*\n\n"
        f"Version: {VERSION}\n"
        "Developed by: Abolfazl Rezaie\n"
        "Purpose: Connecting renters with properties\n"
        "Contact: @VlanSupport\n\n"
        "This bot helps you find and post rental ads easily!"
    )
    bot.reply_to(message, about_text, parse_mode='Markdown')

# Text message handler
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🏠 Open Rentals":
        bot.reply_to(
            message, 
            "Access the rentals app below:",
            reply_markup=get_inline_keyboard()
        )
    elif message.text == "ℹ️ Help":
        help_command(message)
    elif message.text == "📄 About":
        about_command(message)
    else:
        bot.reply_to(
            message,
            "Please use the menu buttons or commands (/start, /help, /about)",
            reply_markup=get_main_menu()
        )

# Error handler
def handle_error(e):
    logger.error(f"Bot error: {str(e)}")
    # You can add notification to admin here if needed

# Start bot with error handling
if __name__ == "__main__":
    try:
        logger.info("Starting bot...")
        bot.infinity_polling()
    except Exception as e:
        handle_error(e)
        logger.error("Bot crashed, restarting in 5 seconds...")
        import time
        time.sleep(5)
        bot.infinity_polling()