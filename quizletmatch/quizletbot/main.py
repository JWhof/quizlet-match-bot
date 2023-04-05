import codecs
import time

import pyautogui
import pyocr
from PIL import Image

lang = 'eng'

tool = pyocr.get_available_tools()[0]

line_box_builder = pyocr.builders.LineBoxBuilder()
text_builder = pyocr.builders.TextBuilder()
line_box_dict = {}

def capture_screenshot(filename):
    time.sleep(3)  # wait for 3 seconds before capturing the screenshot
    pyautogui.press('enter')
    time.sleep(0.3)
    screenshot = pyautogui.screenshot(region=(400,310,4070,2210))

    print(f"pyauto width, height: {screenshot.size}")
    screenshot.save(filename)
    return Image.open(filename)

def scale_line_box_position(line_box, scale_factor):
    x1, y1 = line_box.position[0]
    x2, y2 = line_box.position[1]

    scaled_x1 = int(x1 * scale_factor)
    scaled_y1 = int(y1 * scale_factor)
    scaled_x2 = int(x2 * scale_factor)
    scaled_y2 = int(y2 * scale_factor)

    return ((scaled_x1, scaled_y1), (scaled_x2, scaled_y2))


def line_box_to_pyautogui_position(line_box):
    x1, y1 = line_box.position[0]
    x2, y2 = line_box.position[1]

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    return center_x, center_y


def perform_matching(line_box_coords):
    print(f"line box coords: {line_box_coords}")
    pyautogui.moveTo(line_box_coords[0], line_box_coords[1])
    pyautogui.click(line_box_coords[0], line_box_coords[1])
    return

def main():
    process_duration = 5 
    start_time = time.time()

    screenshot_filename = 'quizletbot/screenshot.png'
    image = capture_screenshot(screenshot_filename)

    print(f"pyorc width, height: {image.size}")

    line_boxes = tool.image_to_string(
        image,
        lang=lang,
        builder=line_box_builder
    )
    
    txt = tool.image_to_string(
    image,
    lang=lang,
    builder=text_builder
    )

    line_box_dict = {line_box.content:line_box.position for line_box in line_boxes}

    perform_matching(line_box_to_pyautogui_position(line_boxes[0]))

    # potential delay? idk man
    time.sleep(1)

    # all of this is mostly for testing
    line_box_tuples = '\n'.join([f"{line_box.content}, {line_box.position}" for line_box in line_boxes])

    with codecs.open("output.txt", 'w', encoding='utf-8') as file_descriptor:
        text_builder.write_file(file_descriptor, line_box_tuples)

    print("done")
    elapsed_time = time.time() - start_time
    if elapsed_time < process_duration+3:
        time.sleep(process_duration+3 - elapsed_time)

    print(line_box_dict)


if __name__ == "__main__":
    main()
