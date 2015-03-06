# Scrapes the html list of all available sections, outputting a json file with
# the organized information.

from lxml import html
import pprint
import json


# Convert time from 12 hour to 24 hour format
def convert_time(time):
    converted = []
    split = time.split('-')

    for t in split:
        # am or pm
        mode = t[-2:]

        t = int(t[:-3].replace(':', ''))

        if t >= 100 and t < 1200 and mode == 'pm':
            t += 1200
        if t >= 1200 and mode == 'am':
            t -= 1200
        converted.append(t)
    return converted

pp = pprint.PrettyPrinter(indent=4)

with open('data/classes.html') as f:
    content = f.read()

tree = html.fromstring(content)

rows = tree.xpath('//tr')

sections = []

z = 0
for row in rows:
    z += 1
    valid = True
    section = []
    if len(row) == 24:
        for i, cell in enumerate(row[:-1]):
            if cell.get('class') != 'dddefault':
                valid = False
                break
            else:
                if cell.text is None:
                    if cell[0].text == 'TBA' and i == 9:
                        valid = False
                    else:
                        section.append(cell[0].text)
                elif cell.text[-1] == '(':
                    section.append(cell.text[:-2])
                else:
                    section.append(cell.text)
        if valid:
            sections.append(section)

structured = {}

last_section = {}
for section in sections:
    # Convert time from text to integer format
    start, end = convert_time(section[9])
    # Keep pretty time format
    p_start, p_end = section[9].split('-')

    # Section has no teacher?
    if len(section) == 18:
        section.append('')
        section.append('TBA')
    # Check if section is blank
    # If so, add to previous section
    if section[2] == u'\xa0':
        if len(section[8]) > 1:
            for day in section[8]:
                if day not in last_section['days']:
                    last_section['days'][day] = {
                        'start': start, 'end': end,
                        'p_start': p_start, 'p_end': p_end,
                        'instructor': section[19]}
                else:
                    last_section['days'][day] = [
                        last_section['days'][day], {
                            'start': start, 'end': end,
                            'p_start': p_start, 'p_end': p_end,
                            'instructor': section[19]}]
        else:
            if section[8] not in last_section['days']:
                    last_section['days'][section[8]] = {
                        'start': start, 'end': end,
                        'p_start': p_start, 'p_end': p_end,
                        'instructor': section[19]}
            else:
                last_section['days'][section[8]] = [
                    last_section['days'][section[8]], {
                        'start': start, 'end': end,
                        'p_start': p_start, 'p_end': p_end,
                        'instructor': section[19]}]
    # If not, treat like regular section
    else:
        # Check if department does not exist
        if section[2] not in structured:
            structured[section[2]] = {}
        # Check if course does not exist
        if section[3] not in structured[section[2]]:
            structured[section[2]][section[3]] = {}
        s = {}
        s['CRN'] = section[1]
        s['credits'] = section[6]
        s['title'] = section[7]
        s['days'] = {}

        if len(section[8]) > 1:
            for day in section[8]:
                s['days'][day] = {
                    'start': start, 'end': end,
                    'p_start': p_start, 'p_end': p_end,
                    'instructor': section[19]}
        else:
            s['days'][section[8]] = {
                'start': start, 'end': end,
                'p_start': p_start, 'p_end': p_end,
                'instructor': section[19]}

        structured[section[2]][section[3]][section[4]] = s

        last_section = s

output = open('data/classes.json', 'w')
json.dump(structured, output)
output.close()

print('Success!')

# 1-CRN
# 2-Department
# 3-Course Number
# 4-Section Number
# 5-Campus (x)
# 6-Credits
# 7-Class Name
# 8-Days
# 9-Time
# 10-Cap
# 19-Instructor
# 20-Date(x)
# 21-Location(x)
