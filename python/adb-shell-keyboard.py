import os
import sys

def run_command(_input):
    new_input = _input.split('&&')
    for input_index in range(len(new_input)):
        new_str = new_input[input_index].split(' ')
        for i in range(len(new_str)):
            if len(new_str[i]) > 0:
                os.system(f"adb shell input text {new_str[i]}")
                os.system("adb shell input keyevent 'KEYCODE_SPACE'")
            else:
                continue

        # os.system(f"adb shell input text {string}")
        os.system("adb shell input keyevent 'KEYCODE_ENTER'")


while 1:
    string = input(">> ")
    if string.lower() in ["quit", "q", "exit"]:
        break
    else:
        run_command(string)

