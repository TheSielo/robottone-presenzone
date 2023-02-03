from telegram import Update

def getId(update: Update):
    return str(update.effective_user.id)