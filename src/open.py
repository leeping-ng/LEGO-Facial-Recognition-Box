import sys

from utils.servomotor import init_servo, rotate_servo
from utils.read_config import extract_config

# read in configuration settings
sys.path.insert(0, '..')
CONFIG_PATH = 'settings.yml'
settings = extract_config(CONFIG_PATH)

# initialize the servo, and rotate it to close the box
init_servo()
rotate_servo(settings['open_angle'])
