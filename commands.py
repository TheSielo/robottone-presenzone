from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from data import runningOperations
from registration import continueRegistration, checkState
from stUtils import getId
from strings import START_EXPLANATION
from preferences import setMode, getMode, loadConfig, getUserFile
from preferences import MODE_INSERTING, MODE_EDITING, MODE_NOTHING, MODE_DELETING, KEY_STATE, STATE_REGISTERED
from keyboards import dayKeyboard, hoursKeyboard, minutesKeyboard, ferieKeyboard
from spreadsheet import writeToday, TYPE_NO_REMAINING
import bot

#Show handy instruction about using this bot.
def start(update: Update, context: CallbackContext):
    update.message.reply_text(START_EXPLANATION)

def insert(update: Update, context: CallbackContext):
    userId = getId(update)
    setMode(userId, MODE_INSERTING)
    insertTime(update, context)

#Add time for today
def insertTime(update: Update, context: CallbackContext, userId: str = None):
    if update:
        id = getId(update)
    else:
        id = userId
    
    if checkState(context, id):
        reply_markup = InlineKeyboardMarkup(hoursKeyboard)
        mode = getMode(id)
        if mode == MODE_EDITING:
            text = 'Quante ore hai lavorato quel giorno?'
        else:
            text = 'Quante ore hai lavorato oggi?'
        bot.updater.bot.send_message(chat_id=id, text=text, reply_markup=reply_markup)

def editTime(update: Update, context: CallbackContext):
    userId = getId(update)
    if checkState(context, userId):
        setMode(userId, MODE_EDITING)
        reply_markup = InlineKeyboardMarkup(dayKeyboard)
        message_reply_text = 'Quale giorno vuoi modificare?'
        context.bot.send_message(chat_id=userId, text=message_reply_text, reply_markup=reply_markup)

#Save the selected number of hours and ask for the minutes
def setMinutes(update: Update, context: CallbackContext):
    reply_markup = InlineKeyboardMarkup(minutesKeyboard)
    message_reply_text = 'E quanti minuti?'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_reply_text, reply_markup=reply_markup)

def setType(update: Update, context: CallbackContext):
    reply_markup = InlineKeyboardMarkup(ferieKeyboard)
    message_reply_text = 'Come segno le ore rimanenti?'
    context.bot.send_message(chat_id=getId(update), text=message_reply_text, reply_markup=reply_markup)


def buttonPressed(update: Update, context: CallbackContext):
    userId = getId(update)
    context.bot.delete_message(chat_id=userId, message_id=update.effective_message.message_id)
    
    parts: list[str] = update.callback_query.data.split(':')
    command: str = parts[0]
    value = int(parts[1])

    if command == 'h':
        day = 0
        if userId in runningOperations and 'e' in runningOperations[userId]:
            day = runningOperations[userId]['e']
        runningOperations[userId] = {'h':value, 'e':day}
        setMinutes(update, context)
    elif command == 'm':
        runningOperations[userId]['m'] = value
        hours = runningOperations[userId]['h']
        if int(hours) >= 8:
            runningOperations[userId]['t'] = TYPE_NO_REMAINING
            day = runningOperations[userId]['e']
            writeToday(update, context, day)
        else:
            setType(update, context)
    elif command == 't':
        runningOperations[userId]['t'] = value
        day = runningOperations[userId]['e']
        writeToday(update, context, day)
    elif command == 'e':
        runningOperations[userId] = {'e':int(value)}
        insertTime(update, context)
    elif command == 'd':
        setMode(userId, MODE_DELETING)
        day = 0
        if userId in runningOperations and 'e' in runningOperations[userId]:
            day = runningOperations[userId]['e']
        writeToday(update, context, day)

def sendSheet(update: Update, context: CallbackContext, userId: str = None):
    if update:
        user = getId(update)
    else:
        user = userId

    if checkState(context, user):
        document = open(getUserFile(user), 'rb')
        bot.updater.bot.send_document(chat_id=user, document=document, filename='Foglio presenze.xlsx')

def forwarder(update: Update, context: CallbackContext):
    userId = getId(update)
    state = loadConfig(userId, KEY_STATE)
    if state != None and int(state) < STATE_REGISTERED:
        continueRegistration(update, context, int(state))
    else:
        text = "Usa uno dei comandi disponibili! Se non ti sei ancora registrato, inizia la registrazione con il comando /register!"
        context.bot.send_message(chat_id=userId, text=text)