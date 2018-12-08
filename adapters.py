def get_default_script():
    return [{'exercise_number': 1, 'set_number': 1, 'length': 60}]

def is_script_editor_script_valid(exercises_and_sets):
    #set is invalid if two exercises appear in a row without any sets or if last item is an exercise without sets
    previous_is_exercise = False
    for exercise_or_set in exercises_and_sets:
        if type(exercise_or_set) is str:
            if previous_is_exercise:
                return False
            previous_is_exercise = True
        else:
            previous_is_exercise = False

    if type(exercises_and_sets[-1]) is str:
        return False

    return True


def to_timer_script(exercises_and_sets):
    exercise_number = 0
    set_number = 0
    timer_script = []
    for exercise_or_set in exercises_and_sets:
        if type(exercise_or_set) is str:
            exercise_number += 1
            set_number = 0
        else:
            set_number += 1
            length = exercise_or_set
            timer_script.append({'exercise_number':exercise_number, 'set_number':set_number, 'length':length})
    return timer_script