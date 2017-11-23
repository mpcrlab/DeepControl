from Arduino import Arduino
import os
if not os.path.isfile('controlfunctions.py'):
    os.chdir('/home/mpcr/Desktop/rodrigo/deepcontrol')
from controlfunctions import *

board = Arduino('9600')
print("type: ", type(board))
print("Setting pin 13 to output...")
board.pinMode(13, "OUTPUT")

print("Setting pin 11 to output...")
board.pinMode(11, "OUTPUT")

print("Setting pin 9 to output...")
board.pinMode(9, "OUTPUT")

print("Setting pin 7 to output...")
board.pinMode(7, "OUTPUT")

print("Setting pin 5 to output...")
board.pinMode(5, "OUTPUT")

print("Setting pin 3 to output...")
board.pinMode(3, "OUTPUT")

print("Setting pin 2 to output...")
board.pinMode(2, "OUTPUT")

print("Done configuring board")

send_keys(board, {'right': False, 'space': False, 'shift': False, 'up': False, 'down': False, 'left': False, 'enter': False})
send_keys(board, {'right': False, 'space': False, 'shift': False, 'up': False, 'down': False, 'left': False, 'enter': False})
send_keys(board, {'right': False, 'space': False, 'shift': False, 'up': False, 'down': False, 'left': False, 'enter': False})
send_keys(board, {'right': False, 'space': False, 'shift': False, 'up': False, 'down': False, 'left': False, 'enter': False})
time.sleep(1)

print("Done!")
