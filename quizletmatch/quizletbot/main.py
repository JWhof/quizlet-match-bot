import pyautogui as pag
import time
import pytesseract
from PIL import Image
import re
from difflib import SequenceMatcher

NUM_SECONDS_TO_WAIT = 3 # set number of seconds to wait to enter quizlet match window
CARD_WIDTH_PX = 250 # number of pixels wide that the box can be, modify depending on terms (if you have alot of long terms, make this longer) MAXES OUT AT 250
SCREENSHOT_HEIGHT_PX = 96 # how tall the screenshot will be, modify depending on terms (if you have alot of long terms, make this longer)
CARD_FONT_SIZE_PX = 16 # font size of text in card in px
TIME_TO_DRAG_CARDS = 0.01 # time the program will take to drag cards to one another, dont change
PERCENT_MATCH = 95 # percentage required to match, dont go below like 85 ish otherwise errors
MAX_TIME_SPENT = 10  # specify the max amt of time spent in the quizlet match window

def start_up(): # wait desired number of seconds and display countdown
    for seconds_left in range(NUM_SECONDS_TO_WAIT)[::-1]:
        print(f"{seconds_left+1}...")
        time.sleep(1)
    print("starting.........")
    time.sleep(1)

def card_coordinates(): # get coords of all cards based on image of top left of card
    return pag.locateAll('quizletmatch/quizletbot/top_card3.png', pag.screenshot(), grayscale=True) # coordinates should be shifted right by 2 and down by 1 

def screenshot_region(left, top, file_name): # screenshot a specific region of the file
    return pag.screenshot(file_name, region=(left + 2, top + 1, CARD_WIDTH_PX, SCREENSHOT_HEIGHT_PX)) # region=left, top, width, height

def screenshot_and_convert_all_cards(): # place all cards into tuple with coordinates and text from ocr
    for count, box in enumerate(list(card_coordinates())):
        file_name = f"box_screenshot{count}.png"
        screenshot_region(box.left, box.top, file_name)
        image_of_box_screenshot = Image.open(file_name)
        list_of_coords_and_text_tuples.append((box, pytesseract.image_to_string(image_of_box_screenshot).strip().replace("\n", " ").strip()))

def organize_input(file_name): # make the input file into a dict
    with open(file_name, 'r') as file:
        text = file.read()

    regex = r'^\d+\.\s.*$' # match only lines starting with an integer followed by a dot
    matches = re.findall(regex, text, flags=re.MULTILINE)

    for match in matches:
        match = re.sub(r'^\d+\.\s', '', match) # chuck everything into one nice dict where we can check for values later
        parts = match.strip().split(':')
        if len(parts) == 2:
            term = parts[0].strip()
            definition = parts[1].strip()
            input_list.append((term, definition))


def drag_matched_boxes(): # match all of the boxes together using the values from the input given by the user, drag boxes to each other
    while list_of_coords_and_text_tuples != [] and time.time() <= start_time + MAX_TIME_SPENT:
        for box1 in list_of_coords_and_text_tuples:
            for box2 in list_of_coords_and_text_tuples: # iterate through same list twice to see if right combo is there, def not the most optimal way but havent finished data structures and algos course yet so TODO
                for pair in input_list: # check if texts match as specified in input_list
                    if (SequenceMatcher(None, box1[1], pair[0]).ratio() * 100 >= PERCENT_MATCH and SequenceMatcher(None, box2[1], pair[1]).ratio() * 100 >= PERCENT_MATCH) or\
                        (SequenceMatcher(None, box1[1], pair[1]).ratio() * 100 >= PERCENT_MATCH and SequenceMatcher(None, box2[1], pair[0]).ratio() * 100 >= PERCENT_MATCH): # check if any of the pairs match 
                        pag.moveTo(box1[0].left+37, box1[0].top+36)
                        pag.mouseDown()
                        pag.moveTo(box2[0].left+37, box2[0].top+36, duration=TIME_TO_DRAG_CARDS)
                        pag.mouseUp()
                        print("matched")
                        list_of_coords_and_text_tuples.remove(box1)
                        list_of_coords_and_text_tuples.remove(box2)
                        time.sleep(0.01)

def start_new_match(): # start a new quizlet match session, useful if your set is a bit wack then you can just leave the program running for a while to get best score possible
    pag.moveTo(58,166) # change this to the coordinates of the back button in the match page on your machine
    time.sleep(0.1)
    pag.click()
    time.sleep(0.75)
    pag.moveTo(2016,319) # change this to the coordinates of the 'match' button on the set home page on your machine
    time.sleep(0.1)
    pag.click()
    time.sleep(0.1)


def main():
    global start_time
    global list_of_coords_and_text_tuples
    global input_list
    global matches

    list_of_coords_and_text_tuples = []
    input_list = []
    matches = {}

    start_up()

    start_time = time.time()

    organize_time = time.time()
    organize_input('quizletmatch\input.txt')
    print(f"organize input time: {time.time() - organize_time}")

    pag.press('enter') # auto press enter on 'start game' screen
    time.sleep(0.5)

    ss_time = time.time()
    screenshot_and_convert_all_cards()
    print(f"screenshot and convert time: {time.time() - ss_time}")

    drag_time = time.time()
    drag_matched_boxes()
    print(f"screenshot and convert time: {time.time() - drag_time}")

    print(f"total time: {time.time() - start_time}")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)
        start_new_match()
        

