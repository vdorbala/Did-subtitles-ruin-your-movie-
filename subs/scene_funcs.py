from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, AutoModelForSequenceClassification
from transformers import pipeline
import pdb
import os
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from pprint import pprint


def print_side_by_side(a, b, size=30, space=4):
    while a or b:
        pprint(a[:size].ljust(size) + " " * space + b[:size])
        a = a[size:]
        b = b[size:]

def scene_extract(SEL_MOVIE, SEL_SCENE, SUBLIST, write_file = False, stats=False):

	SCENE_AVG = 50

	DIRS = ['en/', 'fr-en/', 'fr/', 'en-fr/']

	req_lines = defaultdict(list)

	for DIR in DIRS:

		if DIR.strip('/') not in SUBLIST:
			continue

		for movie in sorted(os.listdir(DIR)):

			if not (movie.endswith('.en') or movie.endswith('.txt') or movie.endswith('.fr')):
				continue

			movie_file = open(DIR + movie, 'r')
			movie = movie.split('.')[0]
			if movie not in SEL_MOVIE:
				continue

			data = movie_file.readlines()
			movielen = len(data)
			
			scenenum = int(round(movielen/SCENE_AVG))
			net = 0
			scene = 0

			if stats == True:
				print("Processing movie - {} from {}".format(movie, DIR))
				print("Length of the script is ", movielen)
				print("Number of scenes is ", SCENE_AVG)
				print("Avg. num of lines per scene are ", scenenum)
				print("Required scene number is {}".format(SEL_SCENE))

			req_lines[DIR.strip('/')].append(data[SEL_SCENE*scenenum:SEL_SCENE*scenenum + scenenum])

			if write_file == True:
				with open("{}_scene_{}_{}".format(str(movie), SEL_SCENE, DIR.strip('/')), 'w+') as f:
					f.writelines((req_lines))

	return req_lines


def ksd(df, REQ_SENTS, movie):

	diff = df.diff()
	maxidx = diff.abs().idxmax(axis=1)
	max_scene = int(maxidx[-1])

	minidx = diff.abs().idxmin(axis=1)
	min_scene = int(minidx[-1])

	print("WORST - Scene with maximum sentiment disparity ({} , {}) of {} is {}.".format(df.loc["{}".format(REQ_SENTS[0])][max_scene], df.loc["{}".format(REQ_SENTS[1])][max_scene], diff.loc[REQ_SENTS[1]][max_scene], max_scene))

	print("BEST - Scene with minimum sentiment disparity ({} , {})  of {} is {}.".format(df.loc["{}".format(REQ_SENTS[0])][min_scene], df.loc["{}".format(REQ_SENTS[1])][min_scene], diff.loc[REQ_SENTS[1]][min_scene], min_scene))

	req_scenes_max = scene_extract(movie, max_scene, REQ_SENTS, write_file=False, stats=False)

	for key in req_scenes_max.keys():
	    print("\nWorst performing {} script for scene {} is \n".format(key, max_scene))
	    pprint(req_scenes_max[key])

	req_scenes_min = scene_extract(movie, min_scene, REQ_SENTS, write_file=False, stats=False)

	for key in req_scenes_min.keys():
	    print("\nBest performing {} script for scene {} is \n".format(key, min_scene))
	    pprint(req_scenes_min[key])

	print('\n')
	print_side_by_side(str(req_scenes_max[REQ_SENTS[0]]), str(req_scenes_max[REQ_SENTS[1]]))
	print_side_by_side(str(req_scenes_min[REQ_SENTS[0]]), str(req_scenes_min[REQ_SENTS[1]]))


if __name__ == '__main__':

	# movielist = ['Adam', 'Americano', 'Another Happy Day', 'Birth', 'Bubble', 'Camping', 'Carancho', 'Dark Places', 'Fighting', 'Gabrielle', 'Golden Door', 
	# 'GoldenEye', 'Hector', 'Hitchcock', 'JFK', 'Jackie', 'Margaret', 'Mr Nobody', 'Paranoid Park', 'Paranormal Activity', 'Smiley Face', 'Stone', 'Supernova', 'The Bubble', 'Trainspotting', 'Yamakasi']

	SEL_MOVIE = ['Trainspotting']

	SEL_SCENE = 44

	SUBLIST = ['en', 'fr']

	req_lines = scene_extract(SEL_MOVIE, SEL_SCENE, SUBLIST, write_file=False)