import json

class Script:
    def __init__(self):
        self.exercises = []

    def add_new_exercise(self, exercise_name, ):

    def save_script(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.exercises, file, indent=4)

    def open_script(self, file_name):
        with open(file_name, 'r') as file:
            self.exercises = json.load(file)



