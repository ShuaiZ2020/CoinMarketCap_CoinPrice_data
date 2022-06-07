from urllib import request
import requests
import pyautogui
import time
# print(pyautogui.position())
while True:
    pyautogui.FAILSAFE = False
    pyautogui.click(x=640, y=620)
    print("click")
    time.sleep(5)