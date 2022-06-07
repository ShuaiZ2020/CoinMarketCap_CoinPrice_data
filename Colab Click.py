# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 09:23:10 2022

@author: jhou27
"""

import time
from pynput.mouse import Controller, Button
from pynput.keyboard import Key, Controller

mouse = Controller()
keyboard = Controller()

while True:
  # mouse.click(Button.left,1)
  keyboard.press(Key.ctrl)
  keyboard.press(Key.enter)
  keyboard.release(Key.enter)
  keyboard.release(Key.ctrl)

  print('clicked')
  time.sleep(15)
