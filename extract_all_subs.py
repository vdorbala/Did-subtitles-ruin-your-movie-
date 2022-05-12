import numpy as np
import re
import pandas
import string
import pdb
from collections import defaultdict

import bisect
import re

def compare(s1, s2):
    remove = string.punctuation + string.whitespace
    mapping = {ord(c): None for c in remove}
    return s1.translate(mapping) == s2.translate(mapping)

data = pandas.read_csv('True_List.csv')

movie_list = data["primaryTitle"].to_list()

# pdb.set_trace()

en_file = open('OpenSubtitles.en-fr.en')
fr_file = open('OpenSubtitles.en-fr.fr')

fr_lines = fr_file.readlines()
en_lines = en_file.readlines()

print("Finished reading OpenSubtitles data!")

linedict = defaultdict(list)
movielist = []

with open('OpenSubtitles.en-fr.ids', 'r') as file:
    content = file.read()
# match = re.search('random', content)

print("Finished reading ID file!")

movie_count = 0

while movie_count <= 71:

        movie = np.random.choice(movie_list)
        
        if movie in movielist:
            continue

        if "/" in movie:
            continue


        movie_count +=1
        print("Processing movie number {} - {}".format(movie_count,movie))

        movielist.append(movie)

        nl = [m.start() for m in re.finditer("\n", content, re.MULTILINE|re.DOTALL)]

        imdb_id = int(data[data["primaryTitle"]==movie]["imdb"])

        print("IMDB ID is", imdb_id)

        matches = list(re.finditer(r"({})".format(imdb_id), content, re.MULTILINE|re.DOTALL))

        # st, en = bisect.bisect(nl, matches[0].start()-1), bisect.bisect(nl, matches[-1].end()-1)+1
        # print("Start and end lines are {}, {}".format(st, en))

        # (?# matches = list(re.finditer(r"(new\s+File\(\))", text, re.MULTILINE|re.DOTALL)))
        # match_count = 0
        # for m in matches:
        #     match_count += 1
        #     r = range(bisect.bisect(nl, m.start()-1), bisect.bisect(nl, m.end()-1)+1)
        #     print(re.sub(r"\s+", " ", m.group(1), re.DOTALL), "found on line(s)", *r)
        # print(f"{match_count} occurrences of new File() found in file....")

        # pdb.set_trace()

        line_start = bisect.bisect(nl, matches[0].start()-1)
        line_end = line_start + len(matches)

        fr_subs = fr_lines[line_start:line_end]
        en_subs = en_lines[line_start:line_end]

        # print(en_subs)
        # pdb.set_trace()

        with open('./subs/fr/{}.fr'.format(movie),'wt+', encoding='utf-8') as file:
            print("Writing English subs for {}".format(movie))
            for item in en_subs:
                file.write(item)

        with open('./subs/en/{}.en'.format(movie),'wt+', encoding='utf-8') as file:
            print("Writing French subs for {}".format(movie))
            for item in fr_subs:
                file.write(item)

        print("Wrote {} lines each!".format(len(en_subs)))

en_file.close()
fr_file.close()



        # match_count = 0
        # for m in matches:
        #     match_count += 1
        #     r = range(bisect.bisect(nl, m.start()-1), bisect.bisect(nl, m.end()-1)+1)
        #     st, en = bisect.bisect(nl, m.start()-1), bisect.bisect(nl, m.end()-1)+1
        #     print(re.sub(r"\s+", " ", m.group(1), re.DOTALL), "found on line(s)", *r)
        #     break
        # 

        # for num, line in enumerate(linedata):
        #     imdb_id = int(data[data["primaryTitle"]==movie]["imdb"])
        #     if str(imdb_id) in line:
        #         print("Found line")
        #         linedict[imdb_id].append(num)

    # np.save('sel_movie_lines',linedict)