import telebot

bot = telebot.TeleBot("8689839891:AAFOugQELVKhJrKCDImACwQsuigvPicvX0c")  # توکن رباتت

@bot.message_handler(content_types=['audio', 'document'])
def get_file_id(message):
    if message.audio:
        print("file_id آهنگ:", message.audio.file_id)
        bot.reply_to(message, f"file_id آهنگ:\n`{message.audio.file_id}`", parse_mode="Markdown")
    elif message.document:
        print("file_id فایل:", message.document.file_id)
        bot.reply_to(message, f"file_id فایل:\n`{message.document.file_id}`", parse_mode="Markdown")

print("ربات روشن شد... آهنگ رو برای ربات بفرست")
bot.infinity_polling()