import csv
import os.path
import random

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
        recommendations = []
        for x in range(num_choices):
            chosen_option = self.options[random.randint(0, len(self.options))]
            recommendations.append(chosen_option)
        return recommendations

