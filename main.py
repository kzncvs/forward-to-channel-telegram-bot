from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import db_tools

updater = Updater(token='')  # Place here token for main bot
dispatcher = updater.dispatcher

CHANNEL_NICKNAME = '@kazanmd'


def id_echo(bot, update):
    answer = update.message.chat_id
    bot.send_message(chat_id=update.message.chat_id, text=answer)


def start(bot, update):
    answer = "Send me your photos and i'll publish it into channel. Videos could be shared to, but only less than 5 Mb"
    bot.send_message(chat_id=update.message.chat_id, text=answer)


def new_photo(bot, update):
    sender_nickname = update.message.from_user['username']
    sender_id = update.message.chat_id
    message_id = update.message.message_id
    if db_tools.is_in_list(sender_nickname):
        answer = "You're in my blacklist"
    else:
        bot.forward_message(chat_id=CHANNEL_NICKNAME, from_chat_id=sender_id, message_id=message_id)
        answer = "Success. Your photo is already in a channel."
    bot.send_message(chat_id=sender_id, text=answer, reply_to_message_id=message_id)


def new_video(bot, update):
    sender_nickname = update.message.from_user['username']
    sender_id = update.message.chat_id
    message_id = update.message.message_id
    if db_tools.is_in_list(sender_nickname):
        answer = "You're in my blacklist"
    else:
        video_size = update.message.video.file_size
        if video_size <= 5100000:
            bot.forward_message(chat_id=CHANNEL_NICKNAME, from_chat_id=sender_id, message_id=message_id)
            answer = "Success. Your video is already in a channel."
        else:
            answer = "Only videos less that 5 Mb can be posted"
    bot.send_message(chat_id=sender_id, text=answer, reply_to_message_id=message_id)


id_handler = CommandHandler('id', id_echo)
dispatcher.add_handler(id_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', start)
dispatcher.add_handler(help_handler)

photo_handler = MessageHandler(Filters.photo, new_photo)
dispatcher.add_handler(photo_handler)

video_handler = MessageHandler(Filters.video, new_video)
dispatcher.add_handler(video_handler)

updater.start_polling()
