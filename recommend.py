from sys import argv
from random import shuffle

options = [ "Chick-fil-A",
         "H-mart",
         "Five Guys",
         "panera bread",
         "pressed",
         "Gourmet Indian",
         "Black & Blue",
         "Feng Shui",
         "chipotle",
         "B.GOOD",
         "upper crust",
         "qdoba",
         "McDonald's",
         "tuscan kitchen",
         "Sichuan Gourmet",
         "blaze",
         "clover",
         "cheesecake factory",
         "friendly toast",
         "burger king",
         "border cafe",
         "wegmans",
         "buffalo wild wings",
         "bamboo",
         "flat bread co.",
         "white coconut"]

def recommend(number_of_choices=1, places_to_choose_from=options):
    length = len(places_to_choose_from) - 1

    if (number_of_choices > length):
        return

    shuffle(places_to_choose_from)
    choices = places_to_choose_from[0:number_of_choices]

    choices_lst = list(choices)
    print("You should get food from %s" % ", ".join(choices_lst[:-2] + [", or ".join(choices_lst[-2:])]))

if __name__ == "__main__":
    if len(argv) == 2:
        recommend(int(argv[1]))
    elif len(argv) == 3:
        lst = map(str, argv[2].strip('[]').replace("'","").replace('"','').split(','))
        recommend(int(argv[1]), lst)
    else:
        recommend()
