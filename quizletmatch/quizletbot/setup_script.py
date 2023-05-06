import pyautogui
import time


screen_width, screen_height= pyautogui.size()
board_x, board_y = 3197, 1209
while 1:
    print(f"real position: {pyautogui.position()}, board position: {pyautogui.position()[0] - (screen_width - board_x)+23, pyautogui.position()[1] - (screen_height - board_y)+71}") # 