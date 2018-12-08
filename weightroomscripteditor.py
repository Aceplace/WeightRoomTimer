import tkinter as tk

from utils import seconds_to_minutes_seconds_string

MAX_LENGTH_OF_SET = 590
NUM_ITEMS_PER_ROW = 6

class WeightRoomScriptEditor(tk.Frame):

    def __init__(self, root):
        super(WeightRoomScriptEditor, self).__init__(root)
        self.exercises_and_sets = ['exercise']

        self.grid_rowconfigure(0, weight=1)

        # Container for adding exercises and sets
        add_exercise_set_button_frame = tk.Frame(self)
        add_exercise_set_button_frame.grid(row=0, column=0, sticky='NW')

        tk.Label(add_exercise_set_button_frame,
                 text='Add Exercises and Sets:').grid(row=0, column=0, columnspan=NUM_ITEMS_PER_ROW)
        tk.Button(add_exercise_set_button_frame,
                  text='Add Exercise', command=self.add_exercise).grid(row=1, column=0, columnspan=NUM_ITEMS_PER_ROW)

        length = 10
        while length <= MAX_LENGTH_OF_SET:
            button = tk.Button(add_exercise_set_button_frame,
                      text=seconds_to_minutes_seconds_string(length),
                      command=lambda l=length:self.add_set(l))
            row = (length // 10 - 1) // NUM_ITEMS_PER_ROW + 3
            column = (length // 10 - 1) % NUM_ITEMS_PER_ROW
            button.grid(row=row, column=column, sticky='EW')
            length += 10

        # Container for script display listbox
        sets_frame = tk.Frame(self)
        sets_frame.grid(row=0, column=1, sticky='NS')

        sets_scrollbar = tk.Scrollbar(sets_frame)
        sets_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.exercises_or_sets_lb = tk.Listbox(sets_frame)
        self.exercises_or_sets_lb.pack(fill=tk.Y, expand=True)
        self.exercises_or_sets_lb.configure(yscrollcommand=sets_scrollbar.set)
        sets_scrollbar.configure(command=self.exercises_or_sets_lb.yview)

        # Set up widgets for misc script actions
        misc_items_frame = tk.Frame(self)
        delete_period_btn = tk.Button(misc_items_frame, text='Delete', command=self.delete_exercise_set)
        delete_period_btn.pack()
        self.total_length_lbl = tk.Label(misc_items_frame, text='Total Length: 00:00')
        self.total_length_lbl.pack()
        misc_items_frame.grid(row=0, column=2, sticky='NW')

        self.refresh_sets_lb()

    def add_set(self, length):
        curse_selection = self.exercises_or_sets_lb.curselection()
        if curse_selection:
            index = curse_selection[0] + 1
        else:
            index = len(self.exercises_and_sets)

        self.exercises_and_sets.insert(index, length)
        self.refresh_sets_lb()
        self.exercises_or_sets_lb.selection_set(index, index)
        self.exercises_or_sets_lb.activate(index)

    def delete_exercise_set(self):
        curse_selection = self.exercises_or_sets_lb.curselection()
        if curse_selection:
            curse_selection = curse_selection[0]
            if curse_selection > 0:
                del self.exercises_and_sets[curse_selection]
            self.refresh_sets_lb()
            if curse_selection >= len(self.exercises_and_sets):
                curse_selection -= 1
            if curse_selection >= 0:
                self.exercises_or_sets_lb.selection_set(curse_selection, curse_selection)
                self.exercises_or_sets_lb.activate(curse_selection)

    def add_exercise(self):
        self.add_set('exercise')

    def refresh_sets_lb(self):
        current_exercise = 0
        current_set = 0
        total_time = 0

        self.exercises_or_sets_lb.delete(0, tk.END)

        for exercise_or_set in self.exercises_and_sets:
            if type(exercise_or_set) is str:
                current_exercise += 1
                current_set = 0
                self.exercises_or_sets_lb.insert(tk.END, f'Exercise {current_exercise}')
            else:
                set_length = exercise_or_set
                current_set += 1
                total_time += set_length
                formatted_time = seconds_to_minutes_seconds_string(set_length)
                self.exercises_or_sets_lb.insert(tk.END, f'Set {current_set}       {formatted_time}')

        self.total_length_lbl.configure(text=f'Total Length: {seconds_to_minutes_seconds_string(total_time)}')





if __name__=='__main__':
    root = tk.Tk()
    WeightRoomScriptEditor(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()