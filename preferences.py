import os
from configparser import ConfigParser

# Some simple helper functions to store and load basic
# configuration keys.

SHEET_PATH = 'documents/'

CONFIG_FILE = 'config.ini'
KEY_STATE = 'state'
KEY_USER_NAME = 'user_name'
KEY_MANAGER_NAME = 'manager_name'

STATE_NEW = 1
STATE_USER_NAME = 2
STATE_REGISTERED = 3
STATE_INSERTING = 4
STATE_EDITING = 5

config = ConfigParser()
config.read(CONFIG_FILE)

def getSections():
    return config.sections()

def checkSection(section: str):
    if not config.has_section(section):
        config.add_section(section)
    saveConfig(section, KEY_STATE, STATE_NEW)

# Store a value in preferences.
def saveConfig(section, key, value):
    config.set(section, key, str(value))
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

# Load a value form preferences.
def loadConfig(section, key):
    if config.has_option(section, key):
        return config.get(section, key)
    else:
        return None

def deleteUserConfig(userId: str):
    config.remove_section(userId)
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

def getUserFile(userId: str) -> str:
    if not os.path.exists(SHEET_PATH):
        os.makedirs(SHEET_PATH)

    return SHEET_PATH + userId + '.xlsx'

def getState(userId: str) -> int:
    return int(loadConfig(userId, KEY_STATE))

def setState(userId: str, value: int):
    saveConfig(userId, KEY_STATE, value)
