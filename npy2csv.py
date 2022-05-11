import numpy as np
from collections import defaultdict
import csv

def main():

	for dir in ['fr-en', 'en', 'en-fr', 'fr']:

		datafile = np.load('{}_sentiment.npy'.format(dir), allow_pickle=True).flat[0]
		datalist = datafile.keys()

		with open('./subs/new_moviesents_{}.csv'.format(dir), 'w+') as f:
			writer = csv.writer(f, delimiter='|')
			for value in datalist:
				writer.writerow([str(value), ',', datafile[value]])
		f.close()

if __name__ == '__main__':
	main()