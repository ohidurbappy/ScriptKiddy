from typing import KeysView
import keyboard

import time
# keyboard.press_and_release('shift+s, space')
time.sleep(5)
a=""
with open('main.py') as fp:
    a=fp.read()


lines=a.splitlines()
for line in lines:
    words=line.split(' ')
    for word in words:
        keyboard.write(word,0.1)
        if words.index(word)==-1:
            continue
        else:
            keyboard.press('space')
             
        time.sleep(.3)
    keyboard.press('enter')
    time.sleep(1)

keyboard.write('The quick brown fox jumps over the lazy dog.')

# keyboard.add_hotkey('ctrl+shift+a', print, args=('triggered', 'hotkey'))

# # Press PAGE UP then PAGE DOWN to type "foobar".
# keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))

# # Blocks until you press esc.
# keyboard.wait('esc')

# # Record events until 'esc' is pressed.
# recorded = keyboard.record(until='esc')
# # Then replay back at three times the speed.
# keyboard.play(recorded, speed_factor=3)

# # Type @@ then press space to replace with abbreviation.
# keyboard.add_abbreviation('@@', 'my.long.email@example.com')

# # Block forever, like `while True`.
# keyboard.wait()