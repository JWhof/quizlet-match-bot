# quizlet-match-bot, auto quizlet match solver
uses libs like pytesseract, re, pyautogui, difflib

best time i got with this was 5.9, see if you can optimize it to get it lower
-does not work great with images

# UPDATE: PATCHED
Unfortunately it was patched as quizlet added a light gradient to the background and adding in confidence checks takes alot longer. i will look into a total overhaul when i have time.

# Usage
to use this: 
1. go to the quizlet set home page (where you can see all of the terms listed out)
2. click on the three dots next to the copy button, in the same row where it will state the owner of the set
3. click "print"
4. choose "glossary" as your layout
5. cmd/ctrl a, copy, then paste into input.txt
6. run main.py

# stuff to note
-READ THE COMMENTS FOR THE VARS YOU CAN CHANGE
-you will need to install all the stuff that i imported at the top of main.py
-yes you need to install tesseract ocr
-for the func start_new_match() it has some coordinates that only work for my monitor, use the test_script to determine where these buttons are for yourself.

ENJOY! don't forget to share this with your friends :)
