import csv
import pandas
import matplotlib.pyplot as plt
import re
import numpy as np
from scene_funcs import scene_extract, ksd
from pprint import pprint

def print_side_by_side(a, b, size=30, space=4):
    while a or b:
        pprint(a[:size].ljust(size) + " " * space + b[:size])
        a = a[size:]
        b = b[size:]

def main(set_movie):

    DIRS = ['en', 'fr', 'en-fr', 'fr-en']

    with open('new_moviesents_en.csv', newline='\n') as f:
        reader = csv.reader(f)
        en_data = list(reader)

    with open('new_moviesents_fr.csv', newline='\n') as f:
        reader = csv.reader(f)
        fr_data = list(reader)

    with open('new_moviesents_en-fr.csv', newline='\n') as f:
        reader = csv.reader(f)
        en_fr_data = list(reader)

    with open('new_moviesents_fr-en.csv', newline='\n') as f:
        reader = csv.reader(f)
        fr_en_data = list(reader)

    plot = []

    for num, movie in enumerate(en_data):
        if str(set_movie) in str(movie[0]):
            print("Processing movie - ", movie[0].strip("|"))
            plot.extend([en_data[num][1:-2], fr_data[num][1:-2], en_fr_data[num][1:-2], fr_en_data[num][1:-2]])
            break


    if len(plot) == 0:
        print("Movie not found! :(")
        exit(0)

    plot = [[float(str(re.findall("\d+\.\d+", x)[0])) for x in y] for y in plot]

    df = pandas.DataFrame(plot)

    for i in range(len(DIRS)):
        df.rename(index={int(i): '{}'.format(DIRS[i])}, inplace=True)

    df_req = df.loc[REQ_SENTS]

    if PLOT:
        for SENT in REQ_SENTS:

            plt.plot(df.loc['{}'.format(SENT)], label = '{}'.format(SENT))

        plt.title("{}".format(set_movie))
        plt.legend()
        plt.show()

    return df_req

if __name__ == '__main__':


    # Choose from en, fr, en-fr, fr-en
    REQ_SENTS = ['en', 'fr-en']

    movielist = ['Adam', 'Americano', 'Another Happy Day', 'Birth', 'Bubble', 'Camping', 'Carancho', 'Dark Places', 'Fighting', 'Gabrielle', 'Golden Door', 
    'GoldenEye', 'Hector', 'Hitchcock', 'JFK', 'Jackie', 'Margaret', 'Mr Nobody', 'Paranoid Park', 'Paranormal Activity', 'Smiley Face', 'Stone', 'Supernova', 'The Bubble', 'Trainspotting', 'Yamakasi']
    # Choose from 
    # ['Adam', 'Americano', 'Another Happy Day', 'Birth', 'Bubble', 'Camping', 'Carancho', 'Dark Places', 'Fighting', 'Gabrielle', 'Golden Door', 
    #'GoldenEye', 'Hector', 'Hitchcock', 'JFK', 'Jackie', 'Margaret', 'Mr Nobody', 'Paranoid Park', 'Paranormal Activity', 'Smiley Face', 'Stone', 'Supernova', 'The Bubble', 'Trainspotting', 'Yamakasi']
    
    SET_MOVIES = ['Adam']
    PLOT = True

    for movie in SET_MOVIES:
        df = main(movie)

        ksd(df, REQ_SENTS, movie)
