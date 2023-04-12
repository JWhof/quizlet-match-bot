import pyautogui as pag
import time
import pytesseract
from PIL import Image
import re

NUM_SECONDS_TO_WAIT = 3 # set number of seconds to wait to enter quizlet match window
MAX_CARD_WIDTH_PX = 250 # number of pixels that the box can be
CARD_FONT_SIZE_PX = 16 # font size of text in card in px
list_of_coords_and_text_tuples = []
input_list = []
matches = {}

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
        list_of_coords_and_text_tuples.append((box, pytesseract.image_to_string(image_of_box_screenshot).strip().replace("\n", " ").strip()))

def organize_input(file_name):
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


def drag_matched_boxes():
    #write_output('quizletmatch/quizletbot/card_coords.txt', str(list_of_coords_and_text_tuples))
    for box1 in list_of_coords_and_text_tuples:
        for box2 in list_of_coords_and_text_tuples:
            for pair in input_list: # check if texts match as specified in input_list
                if (box1[1] == pair[0] and box2[1] == pair[1]) or (box1[1] == pair[1] and box2[1] == pair[0]):
                    pag.moveTo(box1[0].left+7, box1[0].top+6)
                    pag.mouseDown()
                    pag.moveTo(box2[0].left+27, box2[0].top+26, duration=0.2)
                    pag.mouseUp()
                    print("matched")
                    list_of_coords_and_text_tuples.remove(box1)
                    list_of_coords_and_text_tuples.remove(box2)
    print(list_of_coords_and_text_tuples)


def drag_matched_boxes_test(box1,box2,pair):
    if (box1[1] == pair[0] and box2[1] == pair[1]) or (box1[1] == pair[1] and box2[1] == pair[0]):
        pag.moveTo(box1[0])
        pag.dragTo(box2[0])
        print("matched")
                


def write_output(output_file_path, text_to_write):
    file = open(output_file_path, 'a')
    file.write(text_to_write)
    file.close()


def main():
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

    



    #write_output('quizletmatch/quizletbot/card_coords.txt', [f"{coords_and_text}\n" for coords_and_text in list_of_coords_and_text_tuples])
    drag_time = time.time()

    drag_matched_boxes()
    print(f"screenshot and convert time: {time.time() - drag_time}")

    print(f"total time: {time.time() - start_time}")


if __name__ == "__main__":
    main()
