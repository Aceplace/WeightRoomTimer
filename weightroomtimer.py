import tkinter as tk

from utils import seconds_to_minutes_seconds_string


class WeightRoomTimer(tk.Frame):
    def __init__(self, root, script, prefs, layout_option='a'):
        super(WeightRoomTimer, self).__init__(root)
        #Initialize interval timer values and preference values
        self.script = script
        self.current_set = 0
        self.time_remaining_in_set = 0
        self.is_playing = False
        self.exercise_set_lbl_size = prefs['exercise_set_lbl_size']
        self.time_lbl_size = prefs['time_lbl_size']

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #Set up interval timer playback widgets
        interval_timer_playback_frame = tk.Frame(self)
        interval_timer_playback_frame.grid_columnconfigure(3, weight=1)
        self.previous_period_btn = tk.Button(interval_timer_playback_frame, text='<<', command=self.previous_period)
        self.previous_period_btn.grid(row=0, column=0, sticky='W')
        tk.Button(interval_timer_playback_frame, text='>', command=self.pause_timer).grid(row=0, column=1, sticky='W')
        self.next_period_btn = tk.Button(interval_timer_playback_frame, text='>>', command=self.next_period)
        self.next_period_btn.grid(row=0, column=2, sticky='W')
        self.interval_timer_slider = tk.Scale(interval_timer_playback_frame, from_=0, to_=1800, showvalue=False,
                                              orient=tk.HORIZONTAL, command=self.slider_update)
        self.interval_timer_slider.grid(row=1, column=0, columnspan=4, sticky='WE')
        interval_timer_playback_frame.grid(row=0, column=0, sticky='NSEW')

        #set up parent frame of the labels displaying the period number and time remaining
        lbls_parent_frame = tk.Frame(self)
        lbls_parent_frame.grid(row=1, column=0, columnspan=2, sticky='NSEW')
        lbls_parent_frame.grid_rowconfigure(2, weight=1)
        lbls_parent_frame.grid_columnconfigure(2, weight=1)

        # Set up space for adjusting label size
        tk.Button(lbls_parent_frame, text='Decrease Excercise/Set Size',
                  command=self.decrease_exercise_set_lbl_size).grid(row=0, column=0, sticky='W')
        tk.Button(lbls_parent_frame, text='Increase Exercise/Set Size',
                  command=self.increase_exercise_set_lbl_size).grid(row=0, column=1, sticky='W')
        tk.Button(lbls_parent_frame, text='Decrease Time Size',
                  command=self.decrease_time_lbl_size).grid(row=0, column=2, sticky='E')
        tk.Button(lbls_parent_frame, text='Increase Time Size',
                  command=self.increase_time_lbl_size).grid(row=0, column=3, sticky='E')

        # Labels for exercise and time remaining
        self.exercise_lbl = tk.Label(lbls_parent_frame, text='Exr: 1', font=('Times', self.exercise_set_lbl_size))
        self.exercise_lbl.grid(row=1, column=0, columnspan=4, sticky='W')
        self.set_lbl = tk.Label(lbls_parent_frame, text='Set: 1', font=('Times', self.exercise_set_lbl_size))
        if layout_option == 'a':
            self.set_lbl.grid(row=1, column=0, columnspan=4, sticky='E')
        else:
            self.set_lbl.grid(row=2, column=0, columnspan=4, sticky='SW')
        self.time_remaining_in_set = self.script[self.current_set]['length']
        self.time_lbl = tk.Label(lbls_parent_frame, text=seconds_to_minutes_seconds_string(self.time_remaining_in_set),
                                 font=('Times', self.time_lbl_size))
        self.time_lbl.grid(row=2, column=0, columnspan=4, sticky='SE')

        #initialize the starting values and sizes of the label widgets
        self.interval_timer_slider.configure(to_=self.time_remaining_in_set - 1)
        self.interval_timer_slider.set(0)
        self.initialize_set()

        #this call back
        self.after(1000, self.on_second)

    def load_script(self, script):
        self.script = script
        self.current_set = 0
        self.is_playing = False
        self.initialize_set()

    def on_second(self):
        #decrement the time and check on end of set
        if self.is_playing:
            self.time_remaining_in_set -= 1
            if self.time_remaining_in_set <= 0:
                self.next_period()
                if self.current_set == 0:
                    self.is_playing = False

        #Update the slider
        self.time_lbl.configure(text=seconds_to_minutes_seconds_string(self.time_remaining_in_set))
        self.interval_timer_slider.configure(state=tk.NORMAL)
        self.interval_timer_slider.set(self.script[self.current_set]['length'] - self.time_remaining_in_set)
        if self.is_playing:
            self.interval_timer_slider.configure(state=tk.DISABLED)

        #callback will invoke itself repeatadely so that it keeps happening
        self.after(1000, self.on_second)

    def initialize_set(self):
        self.time_remaining_in_set = self.script[self.current_set]['length']
        self.interval_timer_slider.configure(to_=self.time_remaining_in_set - 1)
        self.exercise_lbl.configure(text=self.script[self.current_set]['exercise_label'])
        self.set_lbl.configure(text=self.script[self.current_set]['set_label'])

        self.time_lbl.configure(text=seconds_to_minutes_seconds_string(self.time_remaining_in_set))
        self.interval_timer_slider.configure(state=tk.NORMAL)
        self.interval_timer_slider.set(self.script[self.current_set]['length'] - self.time_remaining_in_set)
        if self.is_playing:
            self.interval_timer_slider.configure(state=tk.DISABLED)

    def pause_timer(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.interval_timer_slider.configure(state=tk.DISABLED)
            self.previous_period_btn.configure(state=tk.DISABLED)
            self.next_period_btn.configure(state=tk.DISABLED)
        else:
            self.interval_timer_slider.configure(state=tk.NORMAL)
            self.previous_period_btn.configure(state=tk.NORMAL)
            self.next_period_btn.configure(state=tk.NORMAL)

    def previous_period(self):
        self.current_set -= 1
        if self.current_set < 0:
            self.current_set = len(self.script) - 1
        self.initialize_set()

    def next_period(self):
        self.current_set += 1
        if self.current_set >= len(self.script):
            self.current_set = 0
        self.initialize_set()

    def decrease_exercise_set_lbl_size(self):
        self.exercise_set_lbl_size -= 10
        if self.exercise_set_lbl_size < 10 :
            self.exercise_lbl = 10
        self.exercise_lbl.configure(font=('Times', self.exercise_set_lbl_size))
        self.set_lbl.configure(font=('Times', self.exercise_set_lbl_size))

    def increase_exercise_set_lbl_size(self):
        self.exercise_set_lbl_size += 10
        self.exercise_lbl.configure(font=('Times', self.exercise_set_lbl_size))
        self.set_lbl.configure(font=('Times', self.exercise_set_lbl_size))

    def decrease_time_lbl_size(self):
        self.time_lbl_size -= 10
        if self.time_lbl_size < 10:
            self.time_lbl_size = 10
        self.time_lbl.configure(font=('Times', self.time_lbl_size))

    def increase_time_lbl_size(self):
        self.time_lbl_size += 10
        self.time_lbl.configure(font=('Times', self.time_lbl_size))

    def slider_update(self, new_slider_value):
        self.time_remaining_in_set = self.script[self.current_set]['length'] - int(new_slider_value)
        self.time_lbl.configure(text=seconds_to_minutes_seconds_string(self.time_remaining_in_set))

    def get_prefs_as_dict(self):
        prefs_dict = {'exercise_set_lbl_size': self.exercise_set_lbl_size,
                      'time_lbl_size': self.time_lbl_size }
        return prefs_dict


if __name__=='__main__':
    root = tk.Tk()
    script = [
        {'exercise_label': 'Exr: 1', 'set_label': 'Set: 1', 'length':90},
        {'exercise_label': 'Exr: 1', 'set_label': 'Set: 2', 'length': 90},
        {'exercise_label': 'Exr: 1', 'set_label': 'Set: 3', 'length': 90},
        {'exercise_label': 'Exr: 2', 'set_label': 'Set: 1', 'length': 90},
        {'exercise_label': 'Exr: 2', 'set_label': 'Set: 2', 'length': 60},
        {'exercise_label': 'Exr: 2', 'set_label': 'Set: 3', 'length': 90},
        {'exercise_label': 'Exr: 2', 'set_label': 'Set: 4', 'length': 90},
        {'exercise_label': 'Exr: 3', 'set_label': 'Set: 1', 'length': 90},
        {'exercise_label': 'Exr: 3', 'set_label': 'Set: 2', 'length': 420},
        {'exercise_label': 'Exr: 3', 'set_label': 'Set: 3', 'length': 90},
        {'exercise_label': 'Exr: 4', 'set_label': 'Set: 1', 'length': 90},
        {'exercise_label': 'Exr: 4', 'set_label': 'Set: 2', 'length': 90},
        {'exercise_label': 'Exr: 5', 'set_label': 'Set: 1', 'length': 90},
        {'exercise_label': 'Exr: 5', 'set_label': 'Set: 2', 'length': 90},


    ]

    prefs = {'exercise_set_lbl_size': 120, 'time_lbl_size': 340 }

    WeightRoomTimer(root, script, prefs).pack(fill=tk.BOTH, expand=True)
    root.mainloop()