import lexicalrichness
from lexicalrichness import LexicalRichness
import os
dir_list = os.listdir("fr-en")
# print(dir_list)
# tr_list = os.listdir("fr-en")
# lex = LexicalRichness(text)

for files in dir_list:
    filename = os.path.splitext(files)[0]
    print("Evaluating",files)
    with open("./fr-en-stats/"+filename+"-stats-fr-en.csv",'a') as f:
        # f.write("filmname,\n")
        og_path = os.path.join("fr-en/",files)
        og_file = open(og_path, mode='rt', encoding="utf8").readlines()
        print(filename+"----------")
        # print(og_file[:10])
        # print(t_file[:10])
        total_lines = len(og_file)
        counter = total_lines
        step = int(total_lines/50)+1
        i = 0
        scene_numbers = 0
        print(step)
        print(total_lines)
        print("scenes should be:",int(total_lines/step))
        while i < (total_lines-step):
            print(scene_numbers)
            text = str(og_file[i:(i+step)])
            
            lexog = LexicalRichness(text)
            print(lexog.terms)
            print(lexog.words)
            print(lexog.ttr)
            f.write(str(scene_numbers)+","+str(lexog.ttr)+","+str(lexog.Herdan)+"\n")
            scene_numbers += 1
            i = i+ step
            print(i)
        text = str(og_file[i:total_lines])
        f.write(str(scene_numbers)+","+str(lexog.ttr)+","+str(lexog.Herdan)+"\n")
    f.close
    print("Done with",files)
    
        