import logging
import schedule
import time

from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, filters

#You have to create 'tokens.py' in the same folder as this file, and there declare
#two strings, 'discordToken' and 'telegramToken', and assign them the correct values.
#The file is not commited to avoid uploading the tokens to the git repository.
from tokens import token

from data import runningOperations
from registration import register, deleteUser
from preferences import setMode, getState, getSections
from preferences import MODE_NOTHING, STATE_REGISTERED
from commands import insertTime
import bot
from commands import forwarder, buttonPressed, start, insert, editTime, sendSheet

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot.telegramBot = Bot(token)
bot.updater = Updater(token, use_context=True)  
# Script start
dispatcher = bot.updater.dispatcher

#Analyze all messages that are not commands
forwardHandler = MessageHandler(filters.text & (~filters.command), forwarder)
dispatcher.add_handler(forwardHandler)

# Buttons callback
dispatcher.add_handler(CallbackQueryHandler(buttonPressed))

# /start command
startHandler = CommandHandler('start', start)
dispatcher.add_handler(startHandler)

# /register command
registerHandler = CommandHandler('register', register)
dispatcher.add_handler(registerHandler)

# /delete command
deleteHandler = CommandHandler('delete', deleteUser)
dispatcher.add_handler(deleteHandler)

# /insert command
insertHandler = CommandHandler('insert', insert)
dispatcher.add_handler(insertHandler)

# /edit command
editHandler = CommandHandler('edit', editTime)
dispatcher.add_handler(editHandler)

# /send sheet command
sendSheetHandler = CommandHandler('sendme', sendSheet)
dispatcher.add_handler(sendSheetHandler)

# Start Telegram bot
bot.updater.start_polling()

def sendQuestions():
    users = getSections()
    for user in users:
        state = getState(user)
        if state == STATE_REGISTERED:
            runningOperations.pop(user, None)
            setMode(user, MODE_NOTHING)
            insertTime(None, None, userId=user) 


TIME = '19:00'
schedule.every().monday.at(TIME).do(sendQuestions)
schedule.every().tuesday.at(TIME).do(sendQuestions)
schedule.every().wednesday.at(TIME).do(sendQuestions)
schedule.every().thursday.at(TIME).do(sendQuestions)
schedule.every().friday.at(TIME).do(sendQuestions)

while True:
    schedule.run_pending()
    time.sleep(30)
