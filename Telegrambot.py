import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

bot = telebot.TeleBot("8689839891:AAFOugQELVKhJrKCDImACwQsuigvPicvX0c")  # توکن رباتت رو بذار

# ================== اینجا اطلاعاتت رو پر کن ==================
CHANNELS = [
    "@ShahinNajafi_Archive",          # کانال اول (یا آیدی عددی مثل -100xxxxxxxxxx)
    "@SHN_RADiKAL",          # کانال دوم
]

GROUP = "https://t.me/+UUoXj4TNRyxmZTY0"      # گروه (یا آیدی عددی)
# یا اگه گروه خصوصی هست آیدی عددی بذار مثل -100xxxxxxxxxx



MUSIC_FILE_ID = "b480f93-0455-49b9-ae6d-d776d76c761f"    # file_id آهنگی که گرفتی
# ==========================================================

def is_member(user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def check_all_memberships(user_id):
    for channel in CHANNELS:
        if not is_member(user_id, channel):
            return False
    if not is_member(user_id, GROUP_ID):
        return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if check_all_memberships(user_id):
        bot.send_audio(message.chat.id, MUSIC_FILE_ID, caption="آهنگ مورد نظرت 🎵")
    else:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("عضویت در کانال اول", url=f"https://t.me/{CHANNELS[0].replace('@', '')}"))
        markup.add(InlineKeyboardButton("عضویت در کانال دوم", url=f"https://t.me/{CHANNELS[1].replace('@', '')}"))
        markup.add(InlineKeyboardButton("عضویت در گروه", url=GROUP_LINK))
        markup.add(InlineKeyboardButton("عضو شدم ✅", callback_data="check_join"))

        bot.send_message(
            message.chat.id,
            "برای دریافت آهنگ باید عضو کانال‌ها و گروه زیر بشی:",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join(call):
    user_id = call.from_user.id

    if check_all_memberships(user_id):
        bot.answer_callback_query(call.id, "عضویتت تایید شد ✅")
        bot.send_audio(call.message.chat.id, MUSIC_FILE_ID, caption="آهنگ مورد نظرت 🎵")
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
    else:
        bot.answer_callback_query(call.id, "هنوز عضو همه کانال‌ها و گروه نشدی!", show_alert=True)

print("ربات روشن شد...")
bot.infinity_polling()
