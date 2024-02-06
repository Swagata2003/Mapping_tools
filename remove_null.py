import json

def find_missing_dates(json_file, time_file_path):
    with open(json_file, 'r', encoding='utf-8') as file:
        pid_title_date_data = json.load(file)

    missing_dates = []

    for pid, data in pid_title_date_data.items():
        title, date = data.get('title'), data.get('date')

        if not date or date.isspace():
            # pid has missing or empty date
            missing_dates.append(pid)

    # Search for missing dates in the time file
    with open(time_file_path, 'r', encoding='utf-8') as file:
        time_data = file.readlines()

    for pid in missing_dates:
        # Search for pid in the time data
        for line in time_data:
            if line.startswith(f'{pid}\t'):
                # Extract date from the line
                date_from_file = line.strip().split('\t')[1].strip()

                # Update the date for the missing pid
                pid_title_date_data[pid]['date'] = date_from_file
                break  # Break after finding the first occurrence

    # Save the updated data back to the json file
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(pid_title_date_data, file, indent=4)

# Replace 'pid_title_date.json' and 'time_file_path' with your actual file paths
find_missing_dates('pid_title_date.json', './cit-HepTh-dates.txt/Cit-HepTh-dates.txt')
