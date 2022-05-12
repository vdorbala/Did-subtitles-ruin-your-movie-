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

movie_list = pandas.read_csv('True_List.csv')
imdb_id_file = pandas.read_csv('overlapping.csv')

imdb_id = list(imdb_id_file['IMDB-number'])
titles = list(imdb_id_file['Title'])

sel_movie_list = pandas.read_csv('True_List.csv')
sel_movie_list = list(sel_movie_list['primaryTitle'])

final_list = defaultdict(list)

for movie in sel_movie_list:
    for idx, ref_movie in enumerate(titles):
        if compare(movie, ref_movie):
        	if not final_list[imdb_id[idx]]:
	            final_list[imdb_id[idx]].append((movie))

print(final_list)

pdb.set_trace()

linedict = defaultdict(list)

linedict = np.load('movie_lines_old.npy',allow_pickle=True)
linedict = linedict.item()

movie_ids = list(linedict.keys())

for movie_id in movie_ids:

	# movie_name = str(final_list[movie_id])

	movie_name = " ".join(re.findall("[a-zA-Z]+", movie_name))

	line_start = linedict[movie_id][0]
	line_end = linedict[movie_id][-1]

	en_file = open('OpenSubtitles.en-fr.en')
	fr_file = open('OpenSubtitles.en-fr.fr')

	fr_lines = fr_file.readlines()
	en_lines = en_file.readlines()

	with open('./subs/fr/{}.fr'.format(movie_name),'w+') as file:
		print("Writing English subs for {}".format(movie_name))
		for i, line in enumerate(fr_lines):
		    if i>=line_start and i<=line_end:
		        file.write(line)


	with open('./subs/en/{}.en'.format(movie_name),'w+') as file:
		print("Writing French subs for {}".format(movie_name))
		for i, line in enumerate(en_lines):
		    if i>=line_start and i<=line_end:
		        file.write(line)


	en_file.close()
	fr_file.close()

