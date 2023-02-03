from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler

def register(update: Update, context: CallbackContext):
    print("registration")