import logging
import schedule
import time

from datetime import datetime
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler, MessageHandler, Filters

#You have to create 'tokens.py' in the same folder as this file, and there declare
#two strings, 'discordToken' and 'telegramToken', and assign them the correct values.
#The file is not commited to avoid uploading the tokens to the git repository.
from tokens import token
from data import runningOperations
from registration import register, continueRegistration
from stUtils import getId
import preferences

from openpyxl import load_workbook

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

telegramBot: Bot = Bot(token)
updater = Updater(token=token, use_context=True)  


START_EXPLANATION = '''Per tutti i Marselli che ci seguono da casa:\n\n
/start - Display commands info.\n\n
'''

#Check that makes sense to continue executing the command.
def checkArguments(update, context, hasArgs):
    #This check MUST be used before answering any command to avoid other groups to use this bot
    '''if not str(update.effective_chat.id) == ids.GROUP_ID and not str(update.effective_chat.id) == ids.TEST_GROUP_ID:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Remove this bot from this chat, or prepare to pay for your actions.")
        print('WRONG CHAT USAGE ATTEMPT!!!')
        return False

    #If the command needs some arguments but there's none, inform the user and return False to abort the execution of the command.
    if hasArgs and len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Si ma dammi sti parametri pero\'')
        return False'''

    return True

#Show handy instruction about using this bot.
def start(update: Update, context: CallbackContext):
    if not checkArguments(update, context, False):
        return

    update.message.reply_text("ciao")

#Add time for today
def insertTime(update: Update, context: CallbackContext, userId: str = None):
    
    if update and context and not checkArguments(update, context, False):
        return

    keyboard = [[InlineKeyboardButton('0', callback_data='h:0')],
            [InlineKeyboardButton('1', callback_data='h:1'),
            InlineKeyboardButton('2', callback_data='h:2'),
            InlineKeyboardButton('3', callback_data='h:3'),
            InlineKeyboardButton('4', callback_data='h:4')],

            [InlineKeyboardButton('5', callback_data='h:5'),
            InlineKeyboardButton('6', callback_data='h:6'),
            InlineKeyboardButton('7', callback_data='h:7'),
            InlineKeyboardButton('8', callback_data='h:8')]]
    

    reply_markup = InlineKeyboardMarkup(keyboard)
    message_reply_text = 'Quante ore hai \"lavorato\" oggi?'

    if update:
        id = update.effective_user.id
    else:
        id = userId
    updater.bot.send_message(chat_id=id, text=message_reply_text, reply_markup=reply_markup)
    

#Save the selected number of hours and ask for the minutes
def setMinutes(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton('00', callback_data='m:00'),
            InlineKeyboardButton('15', callback_data='m:15'),
            InlineKeyboardButton('30', callback_data='m:30'),
            InlineKeyboardButton('45', callback_data='m:45')]]


    reply_markup = InlineKeyboardMarkup(keyboard)
    message_reply_text = 'E quanti minuti?'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_reply_text, reply_markup=reply_markup)

def setType(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton('Ferie', callback_data='t:0'),
            InlineKeyboardButton('Malattia', callback_data='t:1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_reply_text = 'Come segno le ore rimanenti?'
    context.bot.send_message(chat_id=getId(update), text=message_reply_text, reply_markup=reply_markup)


def buttonPressed(update: Update, context: CallbackContext):
    userId = getId(update)
    print(update.callback_query.data)
    parts: list[str] = update.callback_query.data.split(':')
    command: str = parts[0]
    value: str = parts[1]
    if command == 'h':
        runningOperations[userId] = {'h':value}
        setMinutes(update, context)
    elif command == 'm':
        runningOperations[userId]['m'] = value
        setType(update, context)
    elif command == 't':
        runningOperations[userId]['t'] = value

        date = datetime.today()
        if date.weekday() == 4:
            text = 'Grazie! A Lunedì!'
        else:
            text = 'Grazie! A domani!'

        writeToday(update, date)
        runningOperations.pop(userId, None)
        context.bot.send_message(chat_id=getId(update), text=text)


def writeToday(update: Update, date: datetime):
    userId = getId(update)
    hours = runningOperations[userId]['h']
    minutes = runningOperations[userId]['m']
    type = runningOperations[userId]['t']

    if minutes == 0:
        remainingHours = str(8 - int(hours))
    else:
        remainingHours = str(7 - int(hours))

    remainingMinutes = str(60 - int(minutes))

    wb = load_workbook(filename='presenze.xlsx')
    ws = wb.worksheets[date.month-1]
    ws.cell(row=date.day+9, column=3).value = ("%s%s" % (hours, convertMinutes(minutes)))
    if type == '0':
        remainingCol = 4
    else:
        remainingCol = 5
    ws.cell(row=date.day+9, column=remainingCol).value = ("%s%s" % (remainingHours, convertMinutes(remainingMinutes)))
    wb.save('presenze.xlsx')
    
def convertMinutes(minutes: str):
    if minutes == '00':
        return ''
    elif minutes == '15':
        return ',25'
    elif minutes == '30':
        return ',50'
    elif minutes == '45':
        return ',75'

def forwarder(update: Update, context: CallbackContext):
    userId = getId(update)
    state = int(preferences.loadConfig(userId, preferences.KEY_STATE))
    if state != None and state < 2:
        continueRegistration(update, context, state)
    else:
        text = "Usa uno dei comandi disponibili!"
        context.bot.send_message(chat_id=userId, text=text)

# Script start
dispatcher = updater.dispatcher

#Analyze all messages that are not commands
forwardHandler = MessageHandler(Filters.text & (~Filters.command), forwarder)
dispatcher.add_handler(forwardHandler)

# /start command
startHandler = CommandHandler('start', start)
dispatcher.add_handler(startHandler)

# /register command
registerHandler = CommandHandler('register', register)
dispatcher.add_handler(registerHandler)

# /insert command
insertHandler = CommandHandler('insert', insertTime)
dispatcher.add_handler(insertHandler)

# Buttons callback
dispatcher.add_handler(CallbackQueryHandler(buttonPressed))

# Start Telegram bot
updater.start_polling()

def sendQuestions():
    users = preferences.getSections()
    for user in users:
       insertTime(None, None, userId=user) 

schedule.every().day.at('20:00').do(sendQuestions)

while True:
    schedule.run_pending()
    time.sleep(30)
