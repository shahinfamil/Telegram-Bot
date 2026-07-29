import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"))

# ================== اطلاعات ==================
CHANNELS = [
    "@ShahinNajafi_Archive",
    "@SHN_RADiKAL",
]

GROUP_ID = -1001249912970
GROUP_LINK = "https://t.me/+UUoXj4TNRyxmZTY0"

MUSIC_FILE_ID = "CQACAgQAAxkBAAFQccRqagU2-hOs7furJOF0jbM43y01zQACTh0AAh81UFPXDBNcoL5aIT0E"
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
