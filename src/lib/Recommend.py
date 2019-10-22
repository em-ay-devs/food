from os import pardir, path
from csv import DictReader
from random import randint
from copy import copy

CSV_FILE = path.join(path.dirname(__file__), pardir, 'configs/restaurant_data.csv')


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
    def make_recommendations(self, num_choices=3, price=None):
        # makes a shallow copy of the options member variable
        if price and price > 0:
            remaining_options = list(filter(lambda x: len(x['price']) == price, self.options))
        else:
            remaining_options = copy(self.options)

        recommendations = []
        options_count = min(num_choices, len(remaining_options))
        for x in range(options_count):
            chosen_option = remaining_options[randint(0, len(remaining_options) - 1)]
            recommendations.append(chosen_option)
            # removes the chosen option from the list so it won't be picked again on further iterations
            remaining_options.remove(chosen_option)
        return recommendations
