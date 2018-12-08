import json
import tkinter as tk

from tkinter import messagebox
from adapters import is_script_editor_script_valid, to_timer_script, get_default_script
from weightroomscripteditor import WeightRoomScriptEditor
from weightroomtimer import WeightRoomTimer


class App(tk.Tk):
    def __init__(self, prefs, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        #initialize passed in values
        self.prefs_dict = prefs

        # Gui Setup
        # Menu setup
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff = 0)
        file_menu.add_command(label='Exit', command=self.on_close)
        menu_bar.add_cascade(label='File', menu=file_menu)

        view_menu = tk.Menu(menu_bar, tearoff = 0)
        self.view_menu_option = tk.IntVar()
        view_menu.add_radiobutton(label='Script Editor', value=1, variable=self.view_menu_option, command=self.change_view)
        view_menu.add_radiobutton(label='Timer', value=2, variable=self.view_menu_option, command=self.change_view)
        self.view_menu_option.set(1)
        menu_bar.add_cascade(label='View', menu=view_menu)
        self.config(menu=menu_bar)

        # Frame set ups
        self.mainframe = tk.Frame(self)
        self.mainframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.frames[WeightRoomScriptEditor] = WeightRoomScriptEditor(self.mainframe)
        self.frames[WeightRoomScriptEditor].grid(row = 0, column = 0, sticky='NSEW')

        self.frames[WeightRoomTimer] = WeightRoomTimer(self.mainframe, get_default_script(), self.prefs_dict)
        self.frames[WeightRoomTimer].grid(row=0, column=0, sticky='NSEW')

        self.current_frame = self.frames[WeightRoomScriptEditor]
        self.current_frame.tkraise()


    def change_view(self):
        if self.view_menu_option.get() == 1:
            if self.frames[WeightRoomTimer].is_playing:
                self.frames[WeightRoomTimer].pause_timer()
            self.current_frame = self.frames[WeightRoomScriptEditor]
        elif self.view_menu_option.get() == 2:
            if is_script_editor_script_valid(self.frames[WeightRoomScriptEditor].exercises_and_sets):
                timer_script = to_timer_script(self.frames[WeightRoomScriptEditor].exercises_and_sets)
                self.frames[WeightRoomTimer].load_script(timer_script)
                self.current_frame = self.frames[WeightRoomTimer]
            else:
                messagebox.showerror('Script Editor Error', 'Invalid Script')
                self.view_menu_option.set(1)
        self.current_frame.tkraise()

    def on_close(self):
        save_prefs(self.frames[WeightRoomTimer].get_prefs_as_dict())
        self.destroy()


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


if __name__=='__main__':
    prefs = load_prefs()
    root = App(prefs)
    root.state('zoomed')
    root.protocol('WM_DELETE_WINDOW', root.on_close)
    root.mainloop()
