import json
import random
from datetime import date
from difflib import SequenceMatcher

from rich.console import Console

console = Console()

def calculate_buckets(day_number, test=False):
    if test:
        return list(range(1, 6))

    buckets_to_test = [1] # always testing yourself on data thats 'every day'

    if day_number % 2 == 0:         # Every Other Day
        buckets_to_test.append(2)

    if day_number % 7 == 0:         # Every Week
        buckets_to_test.append(3)

    if day_number % 14 == 0:        # Every Other Week
        buckets_to_test.append(4)
    
    if day_number % 30 == 0:        # Every Month
        buckets_to_test.append(5)

    return buckets_to_test


def generate_random_indexes(data):
    country_count = len(data)
    
    country_idxs = list(range(country_count))
    random.shuffle(country_idxs)

    return country_idxs

def load_data(filename):
    # Loading Capital City Data
    with open(filename, 'r+') as cap_file:
        data = json.load(cap_file)

    return data

def main(start_date):
    try:
        today = date.today()
        day_number = (today - start_date).days + 1

        # Load Capital City Data
        data = load_data('data/data.json')
        country_idxs = generate_random_indexes(data)
        country_keys = list(data.keys())
        console.print('Capital City Data Loaded! \u2713\n', style='bold green')

        # Ask for Training / Test
        to_test = input('Would you like to enter test mode? (leave blank for Training) : ') != ''
        
        # Create Schedule
        if to_test:
            buckets_to_test = calculate_buckets(day_number, test=True)
        else:
            buckets_to_test = calculate_buckets(day_number, test=False)
        console.print('\nBuckets Calculated! \u2713\n', style='bold green')

        if not to_test:
            console.print(f'\nDay Number : {day_number}\n', style='bold yellow')

        counter = 0
        correct_answers = 0

        # get loop through countries
        for i, idx in enumerate(country_idxs):
            if not to_test and data[country_keys[idx]]['bucket'] not in buckets_to_test:
                continue
            
            counter += 1

            answer = input(f'{counter}. What is the capital city of {country_keys[idx]}? : ')

            # update the data source
            data[country_keys[idx]]['times_asked'] += 1

            if answer.lower() == data[country_keys[idx]]['capital'].lower(): # correct
                correct_answers += 1
                console.print(f'CORRECT \u2713\n', style='bold green')
                data[country_keys[idx]]['correct_count'] += 1
                if data[country_keys[idx]]['bucket'] + 1 < 5:
                    data[country_keys[idx]]['bucket'] += 1
            else:                                                            # incorrect
                console.print(f'INCORRECT \u274C', style='bold red')
                console.print(f"Correct answer is [bold yellow]{data[country_keys[idx]]['capital']}[bold yellow]\n")
                data[country_keys[idx]]['bucket'] = 1
            
            data[country_keys[idx]]['date_last_asked'] = today.strftime("%Y-%m-%d")      

        if to_test:
            console.print(f'Correct Answers : {correct_answers}! \u2713\n', style='bold green')
        else:
            console.print(f'Day {day_number} Testing Complete! \u2713\n', style='bold green')
            console.print(f'Correct Answers : {correct_answers}! \u2713\n', style='bold green')

            # write results back to json file
            with open("data/data.json", "w") as write_file:
                json.dump(data, write_file)

            console.print('Data successfully recorded! \u2713\n', style='bold green')

    except Exception as e:
        print(e)

if __name__ == '__main__':
    START_DATE = date(2022, 4, 4)

    main(START_DATE)
