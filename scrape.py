# from pythonopensubtitles.opensubtitles import OpenSubtitles
# from pythonopensubtitles.utils import File
import csv
import re
import requests
import difflib

#from pyopensubs import open_subtitles
#from pyopensubs import FileOperations

def get_overlap(s1, s2):
    s = difflib.SequenceMatcher(None, s1, s2)
    pos_a, pos_b, size = s.find_longest_match(0, len(s1), 0, len(s2)) 
    return s1[pos_a:pos_a+size]

def getNumbers(str):
    array = re.findall(r'[0-9]+', str)
    return array

def main():

	#ost = OpenSubtitles() 
	#ost.login('gammaumd', 'Gammaumd!1')


	# Extracting data from the csv files 

	fr_file = open('french_films.csv')
	en_file = open('english_films.csv')

	fr_csv = csv.reader(fr_file)
	en_csv = csv.reader(en_file)

	fr_filmdata = []
	en_filmdata = []

	fr_films = []
	en_films = []

	fr_years = []
	en_years = []

	all_films = []
	all_years = []

	for row in fr_csv:
		fr_filmdata.append(row)

	for row in en_csv:
		en_filmdata.append(row)

	fr_films = [fr_filmdata[i][0] for i in range(len(fr_filmdata))][1:]
	en_films = [en_filmdata[i][0] for i in range(len(en_filmdata))][1:]

	fr_years = [fr_filmdata[i][1] for i in range(len(fr_filmdata))][1:]
	en_years = [en_filmdata[i][1] for i in range(len(en_filmdata))][1:]

	all_films = list(fr_films + en_films)
	all_years = list(fr_years + en_years)

	fr_file.close()
	en_file.close()


	# Finding overlapping films in both sets.

	# 1410 Overlaps, 1485 Total films.
	sel_films = list(set(all_films))

	film_info = [[0 for i in range(2)] for j in range(len(all_films))]

	for i in range(len(all_years)):
		film_info[i][0] = all_years[i]
		film_info[i][1] = all_films[i]

	sel_film_info = set(list(set(map(tuple,film_info))))

	# file_info = ost.get_subtitle_file_info(str(sel_films[0]), "en", True)


	# Pre-processing the aligned OpenSubtitles file for matches with dataset.

	id_file = open('OpenSubtitles.en-fr.ids')
	numlist = []
	movielist = []
	i = 0

	# Convenience variables to set start and end points (Dataset is 41M rows long).
	start_id = 0 # Set to 0, to start checking with all data.
	linerange = float('inf') # Set to float('inf'), to process all data.
	skipfactor = 1000 # Number of rows to skip between dialogues. 10K seems to ensure most movies are covered.

	for row in id_file:
		i+=1
		row = row.split()[0]
		if i<= start_id:
			continue
		if (i%skipfactor == 0):
			print("Checking row {}/41763489".format(i))
			nums = getNumbers(row)
			if nums[1] not in numlist:
				numlist.append(nums[1])
		if i > start_id + linerange:
			break

	id_file.close()

	print("Number of movies from line {} to {} are {}".format(start_id, i, len(numlist)))


	# Interacting with OpenSubtitles.com API, extracting overlapping movies based on name and year.
 
	headers = {
	    'Api-Key': 'x22uFE99YPq5qOAYtFU2i7nuPlpY70Ci'
	}

	overlap_films = []
	overlap_year = []
	overlap_id = []

	try: 
		for i in range(len(numlist)):

			params = (
			    ('imdb_id', numlist[i]),)

			response = requests.get('https://www.opensubtitles.com/api/v1/subtitles', headers=headers, params=params)

			txt = response.text

			try:
				movie_name = txt[txt.index("title\":\"")+len("title\":\""):txt.index("\",\"movie_name")]
				movie_year = txt[txt.index("year\":")+len("year\":"):txt.index(",\"title\"")]

			except:
				print(txt)
				continue
				
			movielist.append(movie_name)

			# print("Movie is {}, and year is {}".format(movie_name, movie_year))
			for year, film in sel_film_info:
				overlap = get_overlap(movie_name, film)
				if (len(overlap) == len(movie_name)):
					print("Overlapping movies are {}, {}".format(overlap, movie_name))
					print("Year in list is {}. Needed year is {}".format(year, movie_year))
					if int(year) == int(movie_year):
						print("FOUND MATCH!".format(year))
						overlap_films.append(movie_name)
						overlap_year.append(year)
						overlap_id.append(numlist[i])
			
		print("Overlapping movies are {}".format(overlap_films))

	# print("Movie list is {}".format(movielist))
	except:
		with open('overlapping.csv', 'w+') as csvfile:
		    spamwriter = csv.writer(csvfile, delimiter=',',
		                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
		    spamwriter.writerow(['Title', 'Year'])
		    for i in range(len(overlap_films)):
			    spamwriter.writerow(['{}, {}, {}'.format(overlap_films[i], overlap_year[i], overlap_id[i])])

	with open('overlapping.csv', 'w+') as csvfile:
	    spamwriter = csv.writer(csvfile, delimiter=',',
	                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
	    spamwriter.writerow(['Title', 'Year'])
	    for i in range(len(overlap_films)):
		    spamwriter.writerow(['{}, {}, {}'.format(overlap_films[i], overlap_year[i], overlap_id[i])])


if __name__ == '__main__':
	main()