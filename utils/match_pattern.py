import re


def match_pattern(post_data):
    patterns = {
        'date': r'^(0[1-9]|[1-2][0-9]|3[0-1])/(0[1-9]|1[0-2])/\d{4}$',
        'name': r"^[a-zA-Z]+$",
        'last_name': r"^[a-zA-Z]+$",
        'phone_number': r"^\d{9}$",
        'number_of_people': r"^\d+$",
        'reserve_hour': r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$",
        'time_of_reserve': r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
    }

    for post_data_key in list(dict(post_data).keys()):
        if not (re.match(patterns[post_data_key], post_data[post_data_key])):
            return False

    return True
