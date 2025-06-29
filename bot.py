import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Your Bot Token from BotFather
BOT_TOKEN = os.environ.get("8013925344:AAHRLMDII2Ukd3QWAcmQ2sjwV7a8qlQHUUE")

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
    
    # Save image to the "images" directory
    os.makedirs('images', exist_ok=True)
    file_path = f"images/{photo.file_id}.jpg"
    await file.download_to_drive(file_path)
    
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
    await update.message.reply_photo(photo=open(file_path, 'rb'), caption="Here is your uploaded image. Choose a search engine:", reply_markup={'inline_keyboard': search_buttons})

# Main function to run the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handler for the /start command
    application.add_handler(CommandHandler("start", start))

    # Message handler for photos
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
