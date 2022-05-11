import lexicalrichness
from lexicalrichness import LexicalRichness
import os
dir_list = os.listdir("en-fr")
# print(dir_list)
# tr_list = os.listdir("fr-en")
# lex = LexicalRichness(text)
with open("en-fr-stats.csv",'a') as f:
    f.write("filmname,stat-type,stat\n")
    for files in dir_list:
        filename = os.path.splitext(files)[0]
        og_path = os.path.join("en-fr/",files)
        og_file = open(og_path, mode='rt', encoding="utf8").read()
        print(filename+"----------")
        # print(og_file[:10])
        # print(t_file[:10])
        lexog = LexicalRichness(og_file)
        print(lexog.terms)
        print(lexog.words)
        print(lexog.ttr)
        f.write(filename+",numwords,"+str(lexog.words)+"\n")
        f.write(filename+",numterms,"+str(lexog.terms)+"\n")
        f.write(filename+",ttr,"+str(lexog.ttr)+"\n")
        f.write(filename+",Herdanv2,"+str(lexog.Herdan)+"\n")
    f.close
        