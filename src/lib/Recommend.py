import os.path
from csv import DictReader
from random import randint
from copy import copy

CSV_FILE = os.path.abspath('src/configs/restaurant_data.csv')


class Recommend:
    # list of options to choose from when determining recommendations
    options = []

    def __init__(self):
        self.options = self.read_csv()

    # Reads the CSV file, extracts all of the food options, and puts them into a list of dictionary objects.
    @staticmethod
    def read_csv():
        options = []
        with open(CSV_FILE, mode='r') as csv_file:
            reader = DictReader(csv_file)
            line_count = 0
            for row in reader:
                if line_count == 0:
                    line_count += 1
                else:
                    # dictionary object with the column headers in the CSV file
                    option = {
                        'name': row['Name'],
                        'takeout': row['Takeout'],
                        'delivery': row['Delivery'],
                        'distance': row['Distance'],
                        'price': row['Price']
                    }
                    options.append(option)
                    line_count += 1
        return options

    def get_options(self):
        return self.options

    # Randomly selects a given number of recommendations for food places. By default, returns a list with 3
    # recommendations.
    def make_recommendations(self, num_choices=3):
        # makes a shallow copy of the options member variable
        remaining_options = copy(self.options)
        if num_choices > len(remaining_options):
            return []
        recommendations = []
        for x in range(num_choices):
            chosen_option = remaining_options[randint(0, len(remaining_options) - 1)]
            recommendations.append(chosen_option)
            # removes the chosen option from the list so it won't be picked again on further iterations
            remaining_options.remove(chosen_option)
        return recommendations
