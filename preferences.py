from configparser import ConfigParser
from requests import get
from time import time
from sys import maxsize

# Some simple helper functions to store and load basic
# configuration keys.

SECONDS_IN_A_DAY = 86400

CONFIG_FILE = 'config.ini'
KEY_STATE = 'state'
KEY_NAME = 'name'

STATE_NEW = 1
STATE_REGISTERED = 2

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
