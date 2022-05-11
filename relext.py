import csv
import re
import requests
import difflib

def getNumbers(str):
    array = re.findall(r'[0-9]+', str)
    return array


def main():

    movielist = []
    movienames = []
    idlist = []
    
    with open('overlapping.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            movielist.append(row)

        movienames = [movielist[i][0] for i in range(len(movielist))][1:]

    print(movienames)


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
    
    movienames = set(movienames)

    print("Number of movies from line {} to {} are {}".format(start_id, i, len(numlist)))

    headers = {
        'Api-Key': 'x22uFE99YPq5qOAYtFU2i7nuPlpY70Ci'
    }

    for i in range(len(numlist)):

        try:
            params = (
                ('imdb_id', numlist[i]),)

            response = requests.get('https://www.opensubtitles.com/api/v1/subtitles', headers=headers, params=params)

            txt = response.text

            try:
                movie_name = txt[txt.index("title\":\"")+len("title\":\""):txt.index("\",\"movie_name")]
                movie_year = txt[txt.index("year\":")+len("year\":"):txt.index(",\"title\"")]

                print("Checking {}".format(movie_name))

                if movie_name in movienames:
                    print("Adding to list!")
                    idlist.append(numlist[i])

            except:
                print(txt)
                continue
        except:
            continue

    print(idlist)

if __name__ == '__main__':
    main()