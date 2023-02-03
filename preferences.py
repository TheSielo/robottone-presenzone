from configparser import ConfigParser
from requests import get
from time import time
from sys import maxsize

# Some simple helper functions to store and load basic
# configuration keys.

SECONDS_IN_A_DAY = 86400

CONFIG_FILE = 'config.ini'
CONFIG_SECTION = 'main'

config = ConfigParser()
config.read(CONFIG_FILE)

if not config.has_section(CONFIG_SECTION):
    config.add_section(CONFIG_SECTION)

# Store a value in preferences.
def saveConfig(key, value):
    config.set(CONFIG_SECTION, key, str(value))
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

# Load a value form preferences.
def loadConfig(key):
    if config.has_option(CONFIG_SECTION, key):
        return config.get(CONFIG_SECTION, key)
    else:
        return None
