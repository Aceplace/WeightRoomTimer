def seconds_to_minutes_seconds_string(num_seconds):
    num_minutes_string = str(num_seconds // 60)
    num_seconds_string = str(num_seconds % 60) if num_seconds % 60 >= 10 else '0' + str(num_seconds % 60)
    return f'{num_minutes_string}:{num_seconds_string}'