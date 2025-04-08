import telebot
import json
from telebot import types

bot_id = 'SudipxDev'
bot = telebot.TeleBot("YOUR_BOT_TOKEN")
bot.delete_webhook()
bot_username = bot.get_me().username

# Replace with your private channel ID
channel_username = -1002007843813  # <-- Change this to your channel ID

def get_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except:
        return []

def save_data(file_name, data):
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file)
        return True
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    broadcast = get_data(f"{bot_id}-user_id.json")
    if message.from_user.id not in broadcast:
        broadcast.append(message.from_user.id)
        save_data(f"{bot_id}-user_id.json", broadcast)

    user_id = message.from_user.id
    msg = message.text
    chat = message.chat

    try:
        member_status = bot.get_chat_member(channel_username, user_id).status
    except:
        member_status = None

    if member_status not in ["member", "administrator", "creator"]:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✘ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url='https://t.me/your_channel'),
            types.InlineKeyboardButton("✅ Jᴏɪɴᴇᴅ", callback_data='join')
        )
        bot.send_photo(
            chat.id,
            photo='https://t.me/botpostingx/12',
            caption=f"""<b>👋 Hey! <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>

👉 You Need To Join Our Channel To Use This Bot. </b>️""",
            reply_markup=markup,
            parse_mode='HTML'
        )
        return

    if msg == '/start':
        bot.send_message(chat.id, "Send me a file or media to get a shareable link.")
        return

    try:
        param = int(msg.replace('/start', '').strip())
        bot.copy_message(chat.id, from_chat_id=channel_username, message_id=param)
    except:
        pass

@bot.message_handler(content_types=['text', 'photo', 'audio', 'document', 'video', 'animation', 'voice', 'sticker', 'poll'])
def handle_content_types(message):
    if message.text == '/broadcast':
        handle_broadcast_command(message)
        return

    user_id = message.from_user.id
    try:
        member_status = bot.get_chat_member(channel_username, user_id).status
    except:
        member_status = None

    if member_status not in ["member", "administrator", "creator"]:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✘ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url='https://t.me/your_channel'),
            types.InlineKeyboardButton("✅ Jᴏɪɴᴇᴅ", callback_data='join')
        )
        bot.send_photo(
            user_id,
            photo='https://t.me/botpostingx/12',
            caption=f"""<b>👋 Hey !!!
👉 You Need To Join Our Channel To Use This Bot. </b>️""",
            reply_markup=markup,
            parse_mode='HTML'
        )
        return

    copied = bot.copy_message(chat_id=channel_username, from_chat_id=message.chat.id, message_id=message.message_id)
    bot.reply_to(message, f"https://t.me/{bot_username}?start={copied.message_id}")

@bot.callback_query_handler(func=lambda call: call.data == 'join')
def join(call):
    user_id = call.from_user.id
    try:
        member_status = bot.get_chat_member(channel_username, user_id).status
    except:
        member_status = None

    bot.delete_message(call.message.chat.id, call.message.message_id)

    if member_status in ["member", "administrator", "creator"]:
        markupJ = types.InlineKeyboardMarkup(row_width=1)
        markupJ.add(
            types.InlineKeyboardButton("✘ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url='https://t.me/your_channel'),
            types.InlineKeyboardButton("✘ Dᴇᴠᴇʟᴏᴘᴇʀ", url='https://t.me/MrrrAdarsh')
        )
        bot.send_photo(
            user_id,
            photo='https://t.me/botpostingx/12',
            caption=f"""✘ Hey 👋 !!!

✘ This Bot Is For Saving Your Files & Getting Shareable Links.""",
            reply_markup=markupJ,
            parse_mode='HTML'
        )
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✘ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url='https://t.me/your_channel'),
            types.InlineKeyboardButton("✅ Jᴏɪɴᴇᴅ", callback_data='join')
        )
        bot.send_photo(
            user_id,
            photo='https://t.me/botpostingx/12',
            caption=f"""<b>👋 Hey !!!
👉 You Need To Join Our Channel To Use This Bot. </b>️""",
            reply_markup=markup,
            parse_mode='HTML'
        )

@bot.message_handler(commands=['broadcast'])
def handle_broadcast_command(message):
    if message.chat.id != 5417870023:
        return
    msg = bot.send_message(message.chat.id, "<b>Enter the message to broadcast:</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, handle_broadcast_message)

def handle_broadcast_message(message):
    chat_id = message.chat.id
    user_list = get_data(f"{bot_id}-user_id.json")
    if user_list is None:
        bot.send_message(chat_id, "Error: User list not found.")
        return

    success = 0
    fail = 0
    for user_id in user_list:
        try:
            bot.copy_message(chat_id=user_id, from_chat_id=chat_id, message_id=message.message_id)
            success += 1
        except:
            fail += 1

    bot.send_message(chat_id, f"""Broadcast Summary:
Total Users: {len(user_list)}
Success: {success} ✅
Failed: {fail} ❌""")

bot.infinity_polling()
