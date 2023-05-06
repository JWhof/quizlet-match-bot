import pyautogui as pag
import time
import os
import bs4

# stuff to do
# position of path
# position of refresh btn
# position of html only btn
# position of save btn

# change at your own risk
pag.FAILSAFE = False

NUM_SECONDS_TO_WAIT = 3 # set number of seconds to wait to enter quizlet match window

def start_up(): # wait desired number of seconds and display countdown
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
    pag.click()

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

        print(f"card_x, card_y : {card_x, card_y}")
        print(f"card_text: {card_text}")

def main():

    #start_up()
    start_time = time.time()

    pag.press("enter")
    time.sleep(0.01)

    #save_to_html_file()
    time.sleep(1)
    locate_tiles()


    print(f"total time: {time.time() - start_time}")


if __name__ == "__main__":
    main()

