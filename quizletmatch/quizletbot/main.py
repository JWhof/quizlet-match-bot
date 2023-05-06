import pyautogui as pag
import time
import os
import re

# stuff to do
# position of path
# position of refresh btn
# position of html only btn
# position of save btn

# change at your own risk
pag.FAILSAFE = True

NUM_SECONDS_TO_WAIT = 3 # set number of seconds to wait to enter quizlet match window

screen_width, screen_height= pag.size()

board_x, board_y = 3197, 1209 # TODO: automate this

extra_x, extra_y = 220+5, 160+5

DURATION = 0



terms_and_defns = {}
text_and_coords_dict = {}

file_path = "quizletmatch\quizletbot\Match_ Change in populations over time _ Quizlet.mhtml"

def start_up(): # wait desired number of seconds and display countdown
    try:
    # remove the file
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")
    except OSError as e:
        print(f"Error deleting the file: {e}")

    for seconds_left in range(NUM_SECONDS_TO_WAIT)[::-1]:
        print(f"{seconds_left+1}...")
        time.sleep(1)
    print("starting.........")
    time.sleep(1)

def save_to_html_file():
    # Open save menu
    pag.hotkey('ctrl', 's')

    # # Paste new path for HTML file
    # pag.moveTo(2830, 56)
    # pag.click()
    # pag.hotkey('ctrl', 'v')

    # # Refresh path of file 
    # pag.moveTo(3184, 60)
    # pag.click()

    # # Change to HTML only save to load faster
    # pag.moveTo(2430, 650)
    # pag.click()

    # pag.moveTo(2430, 650+17)
    # pag.click()

    # Type name
    # time.sleep(1)
    # pag.press('1')
    # time.sleep(1)
    # Press save btn
    pag.moveTo(3267, 697)
    time.sleep(0.05)
    pag.click()

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
            terms_and_defns[term] = definition
    
    print(f"terms_and_defns: {terms_and_defns}")

def check_match(term, definition):
    if terms_and_defns[term] == definition:
        return True

def locate_tiles():

    # open html file
    file = open(f"quizletmatch/quizletbot/{[file for file in os.listdir('quizletmatch/quizletbot') if 'Match_' in file][0]}", "r")
    output2_file = open("quizletmatch\quizletbot\htmloutpout.txt", 'w')
    html = file.read().split("\n")

    # remove the equals sign at the end of each html file
    for line in html:
        if line.endswith("="):
            html[html.index(line)] = line[:-1]
    
    html = ''.join(html)
    html = html.split("/match", 2)[2].split("------")[0].strip().split("MatchModeQuestionScatterBoard is-ready")[1]\
    .split("erd_scroll_detection_container")[0].split("transform: translate(")[1:]

    

    for card in html:
        output2_file.writelines(card + "\n"*2)
        card_x, card_y = [string.replace("px", "").strip() for string in card.split(");")[0].split(",")]
        card_text = card.split("\"")[2]
        text_and_coords_dict[card_text] = (card_x, card_y)

        print(f"card_x, card_y : {card_x, card_y}")
        print(f"card_text: {card_text}")
    
    print(f"text_and_coords_dict: {text_and_coords_dict}")
    

def match_and_move_tiles():
    organize_input('quizletmatch\input.txt')
    terms = list(terms_and_defns.keys())
    defns = list(terms_and_defns.values())
    texts = list(text_and_coords_dict.keys())

    for text in texts:
        match_found = False
        print(f"text: {text}")
        for term in terms:
            if check_match(term, text):
                print(f"Found term '{term}' to definition '{text}'")
                pag.moveTo(int(text_and_coords_dict[term][0])+extra_x, int(text_and_coords_dict[term][1])+extra_y, duration=DURATION)
                pag.mouseDown()
                pag.moveTo(int(text_and_coords_dict[text][0])+extra_x, int(text_and_coords_dict[text][1])+extra_y, duration=DURATION)
                pag.mouseUp()
                match_found = True
                texts.remove(term)
                
        if not match_found:
            for defn in defns:
                if check_match(text, defn):
                    print(f"Found definition '{defn}' to term '{text}'")
                    pag.moveTo(int(text_and_coords_dict[defn][0])+extra_x, int(text_and_coords_dict[defn][1])+extra_y, duration=DURATION)
                    pag.mouseDown()
                    pag.moveTo(int(text_and_coords_dict[text][0])+extra_x, int(text_and_coords_dict[text][1])+extra_y, duration=DURATION)
                    pag.mouseUp()
                    texts.remove(defn)
                
                





def main():

    start_up()
    start_time = time.time()

    pag.press("enter")
    time.sleep(0.01)

    save_to_html_file()
    time.sleep(1)
    print('saved to html file')

    locate_tiles()
    print('located tiles')

    match_and_move_tiles()
    print('matched and moved tiles')

    print(f"total time: {time.time() - start_time}")


if __name__ == "__main__":
    main()

