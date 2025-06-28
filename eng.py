import numpy as np
import pandas as pd
import os
import time

pd.set_option('display.max_rows', None)

try:
    words = pd.read_csv("words.csv")
except:
    words = pd.DataFrame({"Eng": ["happy","sad","angry"], "Chi": ["開心","傷心","生氣"]})
    words.to_csv("words.csv",index=False)


while True:

    os.system("clear")

    print("Vocab helper\n\nModes:\n1.Quiz\n2.Insert\n3.Delete\n4.Word list\n")

    mode = input("Enter mode:(Input nothing to exit)")

    if mode == "1":
        tested = []

        while True:
            os.system("clear")

            if len(tested) == len(words):
                print("Congrats! You have answered all the questions!")
                input()
                break

            while True:
                word = words.sample(1).iloc[0]
                if word.name not in tested:
                    break

            print(word["Chi"])
            org = word["Eng"].split(" ")
            eng = ""
            for w in org:
                w = w[0] + "_" * (len(w) - 1)
                eng += w + " "

            print(eng)
            timeused = time.time()
            ans = input()
            if ans != "":
                if ans == word["Eng"]:
                    tested.append(word.name)
                    timeused = time.time() - timeused
                    print("\nCorrect!")
                    print(f"Used {timeused: .2f} seconds")
                    print("Rating: " + str(round(min(10.0,10*(len(word["Eng"])/timeused)/4.5),1)) + "/10.0")
                    input()
                else:
                    print("\nWrong!")
                    input()

            else:
                break


    elif mode == "2":
        while True:
            os.system("clear")

            eng = input("English word: ")
            chi = input("Chinese meaning: ")

            if eng == "" or chi == "":
                break

            words = pd.concat([words.reset_index(drop=True),pd.DataFrame({"Eng": [eng], "Chi": [chi]}).reset_index(drop=True)],axis=0,ignore_index=True).drop(words.filter(like="Unnamed").columns,axis=1)
            words.to_csv("words.csv",index=False)

            print("Inserted successfully!")
            input()

    elif mode == "3":
        while True:
            os.system("clear")

            eng = input("Word to delete: ")

            if eng == "":
                break

            if eng in words["Eng"].values:

                wIndex = words[words.Eng == eng].index
                words = words.drop(wIndex,axis=0)

                words = words.drop(words.filter(like="Unnamed"),axis=1)

                words.to_csv("words.csv",index=False)

                print("Deleted successfully")
                input()

            else:

                print("Word not found")
                input()

    elif mode == "4":

        print("\n"*3)
        print(words)
        print("\n"*3)
        input()

    else:
        exit()
