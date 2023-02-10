import os

from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler

import stUtils
import preferences


def register(update: Update, context: CallbackContext):
    userId = stUtils.getId(update)
    preferences.checkSection(userId)
    os.system('cp empty_sheet.xlsx ' + preferences.getUserFile(userId))
    context.bot.send_message(chat_id=userId, text='Ehilà bell\'utentozzo! Come ti chiami?')

def continueRegistration(update: Update, context: CallbackContext, state: int):
    userId = stUtils.getId(update)
    if update.message and update.message.text:
        if state == preferences.STATE_NEW:
            preferences.saveConfig(userId, preferences.KEY_USER_NAME, update.message.text)
            preferences.saveConfig(userId, preferences.KEY_STATE, preferences.STATE_USER_NAME)
            text = 'Qual\'è il nome del tuo responsabile?'

        elif state == preferences.STATE_USER_NAME:
            preferences.saveConfig(userId, preferences.KEY_MANAGER_NAME, update.message.text)
            preferences.saveConfig(userId, preferences.KEY_STATE, preferences.STATE_REGISTERED)
            text = ('Wow! Ma che nome bellissimo!\n\nOgni giorno alle 19:00 ti chiederò ' +
            'un resoconto della giornata e compilerò il tuo Foglione Presenzone in automagico!\n\n' +
            'CIAOOOOOOOOOOOOOOOOOOOO!!! EBBBUONNATAAALEEE!!!!!!')

        context.bot.send_message(chat_id=userId, text=text)

