from os import pardir, path
from csv import DictReader
from random import randint
from itertools import chain

CSV_FILE = path.join(path.dirname(__file__), pardir, 'configs/restaurant_data.csv')


class Recommend:
    # list of options to choose from when determining recommendations
    options = []

    def __init__(self):
        self.options = self.read_csv()

    def get_options(self):
        return self.options

    def get_recommendations(self, num_choices=3):
        # only get recommendations if the number of choices is within the acceptable range
        if 0 <= num_choices <= len(self.options):
            weighted_options = self.generate_weighted_list(self.options)
            return self.__make_recommendations(weighted_options, num_choices, [])
        else:
            return []

    # Randomly selects a given number of recommendations for food places.
    def __make_recommendations(self, options, num_choices, selected):
        if num_choices == 0:
            # returns the selected options when the base case (zero number of choices) is reached
            return selected
        else:
            remaining_options = list(filter(lambda x: x not in selected, options))
            chosen_option = remaining_options[randint(0, len(remaining_options) - 1)]
            selected.append(chosen_option)
            return self.__make_recommendations(options, num_choices - 1, selected)

    # Reads the CSV file, extracts all of the food options, and puts them into a list of dictionary objects.
    @staticmethod
    def read_csv():
        options = []
        with open(CSV_FILE, mode='r') as csv_file:
            reader = DictReader(csv_file)
            line_count = 0
            for row in reader:
                # dictionary object with the column headers in the CSV file
                option = {
                    'name': row['Name'],
                    'takeout': row['Takeout'],
                    'delivery': row['Delivery'],
                    'distance': float(row['Distance']),
                    'price': row['Price'],
                    'weight': int(row['Weight'])
                }
                options.append(option)
                line_count += 1
        return options

    # Creates a weighted list using the 'weight' field from the given options list.
    @staticmethod
    def generate_weighted_list(options):
        # maps each option to a list containing a number of duplicates based on the weight
        mapped_weighted_options = [[x] * x['weight'] for x in options]
        # returns a flattened list representing a "weighted" list of options
        return list(chain.from_iterable(mapped_weighted_options))
