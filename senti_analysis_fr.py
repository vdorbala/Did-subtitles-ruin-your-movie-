from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, AutoModelForSequenceClassification
from transformers import pipeline
import pdb
import os
import numpy as np
from collections import defaultdict
from tqdm import tqdm

# For French Movies Only!

def process(line):

	senti_analysis = nlp(line[:510])[0]

	score = senti_analysis['score']
	label = senti_analysis['label']

	if label=='NEGATIVE':
		score = -1*score

	if int(label.split(' star')[0]) <= 2:
		score = -1*score

	return score

def main():

	for DIR in DIRS:

		movsendict = defaultdict(list)

		for movie in tqdm(sorted(os.listdir(DIR))):

			if not (movie.endswith('.fr') or movie.endswith('.txt')):
				print(movie)
				continue

			print(os.getcwd() + DIR.split('.')[1] + 'sentiments/' + str(movie.split('.')[0]) + '_sentiment.npy')

			if os.path.isfile(os.getcwd() + DIR.split('.')[1] + 'sentiments/' + str(movie.split('.')[0]) + '_sentiment.npy'):

				movsendict[movie] = np.load(os.getcwd() + DIR.split('.')[1] + 'sentiments/' + str(movie.split('.')[0]) + '_sentiment.npy', allow_pickle=True)

				print("Skipping movie - ", movie)
				continue

			movie_file = open(DIR + movie, 'rb')

			movie = movie.split('.')[0]
			print("Processing movie - {} from {}".format(movie, DIR))

			data = movie_file.readlines()
			movielen = len(data)
			
			scenenum = int(round(movielen/SCENE_AVG))
			net = 0
			scene = 0

			print("Length of the script is ", movielen)
			print("Number of scenes is ", SCENE_AVG)
			print("Avg. num of lines per scene are ", scenenum)
			
			for num, line in enumerate(data):
				
				num +=1
				net += process(str(line))
				
				if (num%scenenum)==0:
					print("Sentiment for scene {} is {}.".format(scene, net))
					movsendict[movie].append(net)
					scene += 1
					net = 0

			avg_sent = sum(movsendict[movie])/movielen

			print("Average sentiment for {} is {}".format(movie, avg_sent))

			movsendict[movie].append(avg_sent)

			np.save(DIR + 'sentiments/' + str(movie) + '_sentiment', movsendict[movie])

		np.save(DIR.strip('./subs/') + '_sentiment', movsendict)


if __name__ == '__main__':

	SCENE_AVG = 50

	# FOR French
	# tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine")
	# model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")

	# MULTILINGUAL (EN, FR)
	tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
	model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

	nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, device=1)

	DIRS = ['./subs/fr/', './subs/en-fr/']

	main()