# Main application

import copy
from math import floor
from flask import Flask, send_file, request, render_template
from scheduler import find_combinations, get_sections
app = Flask(__name__)


# Convert a time value to a row position on the schedule table
def convert_time(time):
    hour = int(floor(time) / 100)
    result = (hour - 8) * 12
    result += (time - (hour * 100)) / 5
    return result


@app.route('/')
def index():
    return send_file('static/index.html')


@app.route('/submit')
def submit():
    args = request.query_string.split('&')
    split_args = [arg.split('=')[1] for arg in args]
    classes = split_args[0].upper()

    options = {}

    # Assign start and end times
    if split_args[1] != '':
        options['start'] = int(split_args[1])
    if split_args[2] != '':
        options['end'] = int(split_args[2])
    class_list = [c.split('+') for c in classes.split('%0D%0A')]

    response = find_combinations(class_list, options)

    # If over 100 possible schedules display an error
    if len(response) > 100:
        return str(len(response)) + """
         possible schedules. More than 100, please narrow your search."""

    schedules = []

    # Loop through possible schedules
    for individual in response:
        schedule = {
            'M': [],
            'T': [],
            'W': [],
            'R': [],
            'F': []
        }
        schedules.append(schedule)

        # Make schedule table blank
        for day in schedule.values():
            for x in range(168):
                day.append(0)

        # Fill schedule table with appropriate sections
        for class_type, s in individual.items():
            sections = get_sections(class_type)
            section = sections[s]
            for day, value in section['days'].items():
                values = []
                if type(value) == dict:
                    values.append(value)
                else:
                    values = value

                for block in values:
                    start = convert_time(block['start'])
                    end = convert_time(block['end'])

                    time_span = end - start
                    block['span'] = time_span

                    new_section = copy.deepcopy(section)
                    new_section['course'] = class_type
                    new_section['days'][day] = block
                    new_section['section'] = s

                    schedule[day][start] = new_section
                    filler = [1 for x in range(time_span - 1)]
                    schedule[day][start + 1:start + time_span] = filler

    return(
        render_template(
            'submit.html', number=len(schedules), schedules=schedules
        )
    )

if __name__ == '__main__':
    app.run(debug=True)
