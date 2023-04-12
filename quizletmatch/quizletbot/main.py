import pyautogui as pag
import time



NUM_SECONDS_TO_WAIT = 3 # set number of seconds to wait to enter quizlet match window
MAX_CARD_WIDTH_PX = 250 # number of pixels that the box can be
CARD_FONT_SIZE_PX = 16 # font size of text in card in px


def start_up(): # wait desired number of seconds and display countdown
    for seconds_left in range(NUM_SECONDS_TO_WAIT)[::-1]:
        print(f"{seconds_left+1}...")
        time.sleep(1)
    print("starting.........")
    time.sleep(1)

def card_coordinates(): # maybe add number of terms checker?
    return pag.locateAll('quizletmatch/quizletbot/top_card3.png', pag.screenshot())# coordinates are shifted up 10x10 due to image taken

def write_output(output_file_path, text_to_write):
    file = open(output_file_path, 'w')
    file.writelines(text_to_write)

def main():
    start_up()
    start_time = time.time()
    pag.press('enter') # auto press enter
    time.sleep(0.5)
    write_output('quizletmatch/quizletbot/card_coords.txt', [f"{coords}\n" for coords in list(card_coordinates())])
    print(f"total time: {time.time() - start_time}")

if __name__ == "__main__":
    main()
