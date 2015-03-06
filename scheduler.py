# Take in a list of classes, output schedule possibilities

import json

with open('data/classes.json') as f:
    classes = json.load(f)


# 0 -> Subject (MATH)
# 1 -> Course Number (185)
def get_sections(class_data):
    if isinstance(class_data, str) or isinstance(class_data, unicode):
        class_data = class_data.split(' ')

    return classes[class_data[0]][class_data[1]]


# Checks time conflicts on a certain day
def time_conflict(class1, class2, day):
    class1_times = []
    class2_times = []
    if type(class1['days'][day]) == dict:
        class1_times.append(class1['days'][day])
    else:
        class1_times = class1['days'][day]
    if type(class2['days'][day]) == dict:
        class2_times.append(class2['days'][day])
    else:
        class2_times = class2['days'][day]

    conflict = False
    for c1 in class1_times:
        for c2 in class2_times:
            if c1['end'] > c2['start'] and c1['start'] < c2['end']:
                conflict = True
    return conflict


# Checks if two class sections conflict
def check_conflict(class1, class2):
    conflict = False
    for day in class1['days']:
        if day in class2['days']:
            if time_conflict(class1, class2, day):
                conflict = True
    return conflict


# Options:
# start = Earliest class start time
# end = Latest class end time
def find_combinations(class_list, options={}):
    combinations = []

    # Add sections of first class to combinations
    for section in get_sections(class_list[0]):
        combinations.append({' '.join(class_list[0][0:2]): section})

    # Loop section of other classes
    for class_type in class_list[1:]:
        new_combinations = []
        for combination in combinations:
            for section in get_sections(class_type):
                compatible = True
                for check_class, check_section in combination.items():
                    # Check compatability of section
                    if check_conflict(
                            get_sections(check_class)[check_section],
                            get_sections(class_type)[section]):
                        compatible = False
                # If section is compatible, append to list
                if compatible:
                    new_combination = dict(combination)
                    new_combination[' '.join(class_type[0:2])] = section
                    new_combinations.append(new_combination)
        combinations = new_combinations

    new_combinations = []

    # Filter out unwanted sections (whitelist/blacklist)
    for combination in combinations:
        valid = True
        for c in combination:
            section = combination[c]
            for day in get_sections(c)[section]['days'].values():
                if 'start' in options:
                    if isinstance(day, list):
                        for time in day:
                            if time['start'] < options['start']:
                                valid = False
                    else:
                        if day['start'] < options['start']:
                            valid = False
                if 'end' in options:
                    if isinstance(day, list):
                        for time in day:
                            if time['end'] > options['end']:
                                valid = False
                    else:
                        if day['end'] > options['end']:
                            valid = False

            for class_type in class_list:
                # Check if classes match and filter is applied
                if c == ' '.join(class_type[0:2]) and len(class_type) == 3:
                    class_type[2] = class_type[2].replace(
                        '%2B', '+').replace(
                        '%2C', ',')
                    # Whitelist sections
                    if class_type[2][0] == '+':
                        whitelist = class_type[2][1:]
                        if ',' in whitelist:
                            if section not in whitelist.split(','):
                                valid = False
                        else:
                            if section != whitelist:
                                valid = False
                    # Blacklist sections
                    elif class_type[2][0] == '-':
                        blacklist = class_type[2][1:]
                        if ',' in blacklist:
                            if section in blacklist.split(','):
                                valid = False
                        else:
                            if section == blacklist:
                                valid = False

        if valid:
            new_combinations.append(combination)
    return new_combinations

if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    with open('data/classes.txt') as f:
        content = f.readlines()

    # List of required classes
    class_list = []

    for line in content:
        class_list.append(line.strip().split(' '))

    pp.pprint(find_combinations(class_list))
