import pandas as pd
import string

df = pd.read_csv("all_movies.csv")
print(df.shape)
df = df.drop_duplicates(subset=['primaryTitle'])
df = df[df["diff"]!= 0]
print(df.shape)



overlap_file ="overlapping.csv"
overlap = pd.read_csv(overlap_file, sep=',',low_memory=False)
overlap = overlap.drop_duplicates(subset=['Title'])
print(overlap.shape)


def compare(s1, s2):
    remove = string.punctuation + string.whitespace
    mapping = {ord(c): None for c in remove}
    return s1.translate(mapping) == s2.translate(mapping)



prev = overlap['Title'].tolist()
searchfor = []
for v in prev:
    searchfor.append(v.lstrip())

print("Len of prev",len(prev))
curr = df['primaryTitle'].tolist()
print("Len of curr",len(curr))
final_titles = []
overlap_titles = []
for titleA in prev:
    for titleB in curr:
        if (compare(titleA,titleB)):
            final_titles.append(titleB)
            overlap_titles.append(titleA)

final_titles.remove("2012")
overlap_titles.remove("2012")
new_all_movies =  df[df['primaryTitle'].isin(final_titles)]
new_overlap_movies = overlap[overlap['Title'].isin(overlap_titles)]
print("new all list",new_all_movies.shape)
print("New overlap list",new_overlap_movies.shape)


new_all_movies = new_all_movies.sort_values(by=['primaryTitle']).reset_index()
new_overlap_movies = new_overlap_movies.sort_values(by=['Title']).reset_index()

imdb_codes= new_overlap_movies['IMDB-number']

new_all_movies["imdb"] = imdb_codes
new_all_movies = new_all_movies[['primaryTitle','allorating','imdbrating','genres','diff','imdb']]

new_all_movies.to_csv('True_List.csv', index=False)