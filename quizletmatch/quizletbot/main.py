import pyautogui as pag
import time
import pytesseract
from PIL import Image
import re

NUM_SECONDS_TO_WAIT = 3 # set number of seconds to wait to enter quizlet match window
MAX_CARD_WIDTH_PX = 250 # number of pixels that the box can be
CARD_FONT_SIZE_PX = 16 # font size of text in card in px
dict_of_coords_and_text = {}

def start_up(): # wait desired number of seconds and display countdown
    for seconds_left in range(NUM_SECONDS_TO_WAIT)[::-1]:
        print(f"{seconds_left+1}...")
        time.sleep(1)
    print("starting.........")
    time.sleep(1)

def card_coordinates(): # maybe add number of terms checker?
    return pag.locateAll('quizletmatch/quizletbot/top_card3.png', pag.screenshot())# coordinates should be shifted right by 2 and down by 1 

def screenshot_region(left, top, file_name):
    return pag.screenshot(file_name, region=(left + 2, top + 1, MAX_CARD_WIDTH_PX, 96)) # region=left, top, width, height

def screenshot_and_convert_all_cards():
    for count, box in enumerate(list(card_coordinates())):
        file_name = f"box_screenshot{count}.png"
        screenshot_region(box.left, box.top, file_name)
        image_of_box_screenshot = Image.open(file_name)
        dict_of_coords_and_text[box] = pytesseract.image_to_string(image_of_box_screenshot).replace("\n", " ")

def match_text(file_name):
    with open(file_name, 'r') as file:
        text = file.read()

    regex = r'^\d+\.\s.*$' # match only lines starting with an integer followed by a dot
    matches = re.findall(regex, text, flags=re.MULTILINE)

    word_dict = {}
    for match in matches:
        match = re.sub(r'^\d+\.\s', '', match) # chuck everything into one nice dict where we can check for values later
        parts = match.strip().split(':')
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            word_dict[key] = value

    return word_dict


def write_output(output_file_path, text_to_write):
    file = open(output_file_path, 'w')
    file.writelines(text_to_write)

    
def main():
    start_up()

    start_time = time.time()

    pag.press('enter') # auto press enter on 'start game' screen
    time.sleep(0.5)

    screenshot_and_convert_all_cards()

    write_output('quizletmatch/quizletbot/card_coords.txt', [f"{box}, {dict_of_coords_and_text[box]}\n" for box in dict_of_coords_and_text.keys()])
    print(f"total time: {time.time() - start_time}")


if __name__ == "__main__":
    print(match_text('quizletmatch\input.txt'))
