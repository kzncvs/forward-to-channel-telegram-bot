from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import db_tools

updater = Updater(token='')  # Place here token for ban bot
dispatcher = updater.dispatcher


def id_echo(bot, update):
    answer = update.message.chat_id
    bot.send_message(chat_id=update.message.chat_id, text=answer)


def start(bot, update):
    answer = 'list - Return ban list\nban - ban by nickname\nunban - unban by nickname'
    bot.send_message(chat_id=update.message.chat_id, text=answer)


def get_ban_list(bot, update):
    answer = '\n'.join(db_tools.get_banned_list())
    bot.send_message(chat_id=update.message.chat_id, text=answer)


def new_ban(bot, update):
    target = update.message.forward_from['username']
    db_tools.add_id_to_banned_list(target)
    answer = str(target) + ' has been banned'
    bot.send_message(chat_id=update.message.chat_id, text=answer)


def unban(bot, update):
    target = update.message.text.split(' ')[1]
    if db_tools.is_in_list(target):
        db_tools.del_from_banned_list(target)
        answer = target + ' has been unbanned'
    else:
        answer = target + ' is not in ban list'
    bot.send_message(chat_id=update.message.chat_id, text=answer)


def ban(bot, update):
    target = update.message.text.split(' ')[1]
    db_tools.add_id_to_banned_list(target)
    answer = target + ' has been banned'
    bot.send_message(chat_id=update.message.chat_id, text=answer)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

id_handler = CommandHandler('id', id_echo)
dispatcher.add_handler(id_handler)

get_ban_list_handler = CommandHandler('list', get_ban_list)
dispatcher.add_handler(get_ban_list_handler)

ban_handler = MessageHandler(Filters.forwarded, new_ban)
dispatcher.add_handler(ban_handler)

unban_handler = CommandHandler('unban', unban)
dispatcher.add_handler(unban_handler)

ban_handler = CommandHandler('ban', ban)
dispatcher.add_handler(ban_handler)

updater.start_polling()
