import json
import os
import tkinter as tk

from weightroomtimer import WeightRoomTimer

SCHEDULE_DIRECTORY = r'C:\Users\AcePl\Desktop\WRTQuickLaunch'

# Assumes one properly formatted text file in directory
def get_file_lines():
    directory_items = os.listdir(SCHEDULE_DIRECTORY)
    if len(directory_items) != 1:
        raise Exception('Directory should exactly one item')
    full_path_name = os.path.join(SCHEDULE_DIRECTORY, directory_items[0])
    if not os.path.isfile(full_path_name):
        raise Exception('Directory should only contain one file')

    with open(full_path_name, 'r') as file:
        lines = file.read().splitlines()

    # Clean the list removing blank spaces and white spaces
    lines = [line.strip() for line in lines if line.strip() != '']

    return lines


def parse_file_lines(lines):
    script = []

    if len(lines) == 0 or len(lines) % 2 == 1:
        raise Exception('Incorrect Number of Lines (Should be even)')

    for i, line in enumerate(lines):
        if i % 2 == 0:
            current_exercise_name = line
            continue

        set_time_strings = line.split()
        for j, set_time_string in enumerate(set_time_strings):
            min_sec = set_time_string.split(':')
            if len(min_sec) != 1 and len(min_sec) != 2:
                raise Exception('Incorrectly formatted set times')

            try:
                if len(min_sec) == 1:
                    set_time = int(min_sec[0]) * 60
                else:
                    set_time = int(min_sec[0]) * 60 + int(min_sec[1])

                script.append(
                    {
                    'exercise_label':current_exercise_name,
                    'set_label':f'Set {j + 1}',
                    'length':set_time
                    }
                )
            except ValueError:
                raise Exception('Incorrectly formatted set times')

    return script


def load_prefs():
    try:
        with open('prefs.json', 'r') as file:
            json_prefs_dict = json.load(file)
            file.close()
    except (IOError, json.decoder.JSONDecodeError):
        json_prefs_dict = {'exercise_set_lbl_size': 120, 'time_lbl_size': 340}
    return json_prefs_dict


def save_prefs(prefs_dict):
    file = open('prefs.json', 'w')
    json.dump(prefs_dict, file)
    file.close()


if __name__ == '__main__':
    root = tk.Tk()

    prefs = load_prefs()
    script = parse_file_lines(get_file_lines())
    weightroom_timer = WeightRoomTimer(root, script, prefs, 'b')
    weightroom_timer.pack(fill=tk.BOTH, expand=True)

    def on_close():
        save_prefs(weightroom_timer.get_prefs_as_dict())
        root.destroy()

    root.state('zoomed')
    root.protocol('WM_DELETE_WINDOW', on_close)
    root.mainloop()
