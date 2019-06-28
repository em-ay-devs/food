import csv
import os.path
from random import randint
from copy import copy

CSV_FILE = os.path.abspath('src/configs/restaurant_data.csv')


class Recommend:
    # list of options to choose from when determining recommendations
    options = []

    def __init__(self):
        self.options = self.read_csv()

    @staticmethod
    def read_csv():
        options = []
        with open(CSV_FILE, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            line_count = 0
            for row in reader:
                if line_count == 0:
                    line_count += 1
                else:
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

    def make_recommendations(self, num_choices=3):
        # makes a shallow copy of the options member variable
        remaining_options = copy(self.options)
        recommendations = []
        for x in range(num_choices):
            chosen_option = remaining_options[randint(0, len(remaining_options) - 1)]
            recommendations.append(chosen_option)
            # removes the chosen option from the list so it won't be picked again on further iterations
            remaining_options.remove(chosen_option)
        return recommendations

