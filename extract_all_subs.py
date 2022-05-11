import numpy as np
import re
import pandas
import string
import pdb
from collections import defaultdict

def compare(s1, s2):
    remove = string.punctuation + string.whitespace
    mapping = {ord(c): None for c in remove}
    return s1.translate(mapping) == s2.translate(mapping)

movie_list = pandas.read_csv('final_movies_list_F.csv')
imdb_id_file = pandas.read_csv('overlapping.csv')

imdb_id = list(imdb_id_file['IMDB-number'])
titles = list(imdb_id_file['Title'])

sel_movie_list = pandas.read_csv('final_movies_list_F.csv')
sel_movie_list = list(sel_movie_list['primaryTitle'])

final_list = []

for movie in sel_movie_list:
    for idx, ref_movie in enumerate(titles):
        if compare(movie, ref_movie):
            final_list.append((movie,imdb_id[idx]))

pdb.set_trace()


linedict = defaultdict(list)
movielist = []
with open('OpenSubtitles.en-fr.ids', 'rt') as f:
    for idx, movie in enumerate(final_list):
        if movie in movielist:
            continue
        print(movie)
        movielist.append(movie)

        f.seek(0)
        data = f.readlines()
        for num, line in enumerate(data):
            if str(final_list[idx][1]) in line:
                linedict[final_list[idx][1]].append(num)

np.save('movie_lines_old1',linedict)

pdb.set_trace()
