import pyautogui as pag
import time

NUM_SECONDS_TO_WAIT = 3 # set number of seconds to wait to enter quizlet match window


def card_coordinates(): # maybe add number of terms checker?
    return pag.locateAll('quizletmatch/quizletbot/top_card3.png', pag.screenshot()) # coordinates are shifted up 10x10 due to image taken

def write_output(output_file_path, text_to_write):
    file = open(output_file_path, 'w')
    file.writelines(text_to_write)

def main():
    time.sleep(NUM_SECONDS_TO_WAIT) # wait desired number of seconds 
    print("starting.........")
    start_time = time.time()
    pag.press('enter') # auto press enter

    write_output('quizletmatch\quizletbot\card_coords.txt', [f"{coords}\n" for coords in list(card_coordinates())])
    print(f"total time: {time.time() - start_time}")

if __name__ == "__main__":
    main()
