from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, AutoModelForSequenceClassification
from transformers import pipeline
import pdb
import os
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from pprint import pprint


def print_side_by_side(s1, s2, size=50, space=4):
    # while a or b:
    #     pprint(a[:size].ljust(size) + " " * space + b[:size])
    #     a = a[size:]
    #     b = b[size:]

    maxChars = 50
    maxLength = max(len(s1),len(s2))

    s1 = s1.ljust(maxLength," ")
    s2 = s2.ljust(maxLength," ")

    s1 = [s1[i:i+maxChars] for i in range(0,len(s1),maxChars)]
    s2 = [s2[i:i+maxChars] for i in range(0,len(s2),maxChars)]

    for elem1, elem2 in zip(s1,s2):
        print(elem1.ljust(maxChars," "), end="    ")
        print(elem2)


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

	## SENTIMENT PART

	m = 1 # Worst Scenes 
	n = 1 # Best Scenes
	l1 = 0.5 # Sentiment weight
	l2 = 0.5 # Translationese weight

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


	req_max_list = []
	req_min_list = []

	maxids = list(diff.abs().T.iloc[:,-1].nlargest(m).index)
	minids = list(diff.abs().T.iloc[:,-1].nsmallest(n).index)

	for i in range(m):
		max_scene = maxids[i]

		req_max_list.append(diff.loc[REQ_SENTS[1]][max_scene])

	for i in range(n):
		min_scene = minids[i]

		req_min_list.append(diff.loc[REQ_SENTS[1]][min_scene])


	difflist = list(diff.loc[REQ_SENTS[1]][:])
	avg_sent = sum(list(diff.loc[REQ_SENTS[1]][:]))/len(difflist)

	# print(avg_sent, sum(req_max_list)/m, sum(req_min_list)/n, (sum(req_max_list) + sum(req_min_list))/(m+n))

	senti_transfer = max(avg_sent, (sum(req_max_list) + sum(req_min_list))/(m+n))

	## Translationese PART





	## Final Score
	ksd = l1*senti_transfer + l2*translationese

	return ksd

	# for s1, s2 in zip(req_scenes_max[REQ_SENTS[0]], req_scenes_max[REQ_SENTS[1]]):
	# 	for idx, line in enumerate(s1):
	# 		print_side_by_side(str(s1[idx]), str(s2[idx]))

	# for s1, s2 in zip(req_scenes_min[REQ_SENTS[0]], req_scenes_min[REQ_SENTS[1]]):
	# 	for idx, line in enumerate(s1):
	# 		print_side_by_side(str(s1[idx]), str(s2[idx]))


if __name__ == '__main__':

	# movielist = ['Adam', 'Americano', 'Another Happy Day', 'Birth', 'Bubble', 'Camping', 'Carancho', 'Dark Places', 'Fighting', 'Gabrielle', 'Golden Door', 
	# 'GoldenEye', 'Hector', 'Hitchcock', 'JFK', 'Jackie', 'Margaret', 'Mr Nobody', 'Paranoid Park', 'Paranormal Activity', 'Smiley Face', 'Stone', 'Supernova', 'The Bubble', 'Trainspotting', 'Yamakasi']

	SEL_MOVIE = ['Trainspotting']

	SEL_SCENE = 44

	SUBLIST = ['en', 'fr']

	req_lines = scene_extract(SEL_MOVIE, SEL_SCENE, SUBLIST, write_file=False)