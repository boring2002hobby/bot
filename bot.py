import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import Dispatcher

# Set up Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Bot Token from BotFather
BOT_TOKEN = os.environ.get("8013925344:AAHRLMDII2Ukd3QWAcmQ2sjwV7a8qlQHUUE")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set!")
    exit(1)

# Initialize the Telegram Bot application
application = Application.builder().token(BOT_TOKEN).build()
dispatcher = application.updater.dispatcher

# Start command handler
async def start(update: Update, context):
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(f"Hello {user_first_name}! Please upload the photo you want to search.")

# Function to handle photo uploads
async def handle_photo(update: Update, context):
    chat_id = update.message.chat.id
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_url = file.file_url
    
    # Respond with the uploaded photo and search buttons
    search_buttons = [
        [
            {
                'text': '🔍 Yandex',
                'url': f'https://yandex.com/images/search?rpt=imageview&url={file_url}'
            },
            {
                'text': '🔍 Google',
                'url': f'https://lens.google.com/uploadbyurl?url={file_url}'
            }
        ],
        [
            {
                'text': '🔍 Bing',
                'url': f'https://www.bing.com/images/search?q=imgurl:{file_url}&view=detailv2&iss=sbi&FORM=IRSBIQ'
            },
            {
                'text': '🔍 TinEye',
                'url': f'https://tineye.com/search?url={file_url}'
            }
        ],
        [
            {
                'text': '🔍 SauceNAO',
                'url': f'https://saucenao.com/search.php?url={file_url}'
            }
        ]
    ]
    
    # Send the uploaded photo and buttons
    await update.message.reply_photo(photo=file_url, caption="Here is your uploaded image. Choose a search engine:", reply_markup={'inline_keyboard': search_buttons})

# Main function to set up command handlers
def setup_handlers():
    # Command handler for the /start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Message handler for photos
    dispatcher.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# Set up the webhook endpoint for the serverless function
@app.route('/webhook', methods=['POST'])
def webhook():
    # This gets the incoming update from Telegram
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, application.bot)
    
    # Process the update (use the dispatcher to handle the update)
    dispatcher.process_update(update)
    
    return "OK", 200

# The entry point for the serverless function
def handler(event, context):
    setup_handlers()
    return app(event, context)

# Required for Vercel to run the app correctly
if __name__ == "__main__":
    app.run(debug=True)
