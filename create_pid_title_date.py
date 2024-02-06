


import os
import re
import json
from datetime import datetime


def findfile_name(str):
    if str=="92":
        return "1992"
    elif str=="93":
        return "1993"
    elif str=="94":
        return "1994"
    elif str=="95":
        return "1995"
    elif str=="96":
        return "1996"
    elif str=="97":
        return "1997"
    elif str=="98":
        return "1998"
    elif str=="99":
        return "1999"
    elif str=="00":
        return "2000"
    elif str=="01":
        return "2001"
    elif str=="02":
        return "2002"
    elif str=="03":
        return "2003"
    return "null"
def parse_date(date_str):
    try:
        # Try parsing with the full year format
        return datetime.strptime(date_str, '%d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
    except ValueError:
        try:
            # If that fails, try parsing with the abbreviated year format
            return datetime.strptime(date_str, '%d %b %y %H:%M:%S %z').strftime('%Y-%m-%d')
        except ValueError:
            # If both formats fail, handle the case of missing month or date
            parts = date_str.split()
            if len(parts) == 6:
                day, month, year, time, timezone = parts[0], 'Jan', parts[2], parts[3], parts[4]
                try:
                    return datetime.strptime(f'{day} {month} {year} {time} {timezone}', '%d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
                except ValueError:
                    return ""
            elif len(parts) == 5:
                day, month, year, time, timezone = parts[0], 'Jan', parts[1], parts[2], parts[3]
                try:
                    return datetime.strptime(f'{day} {month} {year} {time} {timezone}', '%d %b %y %H:%M:%S %z').strftime('%Y-%m-%d')
                except ValueError:
                    return ""
            else:
                return ""
               
def extract_title_and_pid_and_date(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    title_match = re.search(r'Title:(.+?)Authors:', content, re.DOTALL)
    pid_match = re.search(r'hep-th/(\d+)', content)
    date_match = re.search(r'Date:\s*([^\s]+)\s*(\d{1,2} [a-zA-Z]+ \d{2,4} \d{2}:\d{2}:\d{2} [+-]\d{4})', content)

    if title_match and pid_match:
        title = title_match.group(1).replace('\n', ' ').strip()
        pid = pid_match.group(1)
        date_str = date_match.group(2) if date_match else None

        if date_str:
            # Convert date string to datetime object
            
                formatted_date= parse_date(date_str)

            # Convert to the desired format
            # formatted_date = date_object.strftime('%Y-%m-%d')

        else:
            formatted_date = None

        return title, pid, formatted_date
    else:
        return None, None, None


def process_directory(directory, output_file):
    paper_data = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.abs'):
                file_path = os.path.join(root, file)
                title, pid,date = extract_title_and_pid_and_date(file_path)
                if title and pid:
                    paper_data[pid] = {
                        'title': title,
                        'date': date
                    }

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(paper_data, json_file, indent=4)

# Replace 'your_main_directory' and 'output.json' with your actual directory and desired output file name.
main_directory = './cit-HepTh-abstracts'
output_file = 'pid_title_date.json'

process_directory(main_directory, output_file)
print(f"JSON file created successfully")
