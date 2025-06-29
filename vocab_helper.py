import numpy as np
import pandas as pd
import os
import time
import json



def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")




pd.set_option('display.max_rows', None)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


try:
    words = pd.read_csv("words.csv")
except:
    words = pd.DataFrame({"Eng": ["happy","sad","angry"], "Chi": ["開心","傷心","生氣"], "POS": ["adj.","adj.","adj."]})
    words.to_csv("words.csv",index=False)

try:
    with open("config.json","r") as file:
        config = json.load(file)
except:
    config = {"tpSpeed": 4.5, "blindMode": False, "showAns": True}
    with open("config.json","w") as file:
        json.dump(config,file)



while True:

    clr()

    words = words.fillna("Unknown")

    print("Vocab helper\n\nModes:\n1.Quiz\n2.Insert\n3.Delete\n4.Word list\n5.Settings\n")

    mode = input("Enter mode (Input nothing to exit): ")

    if mode == "1":
        tested = []
        ratings = []
        allt = 0
        count = 1
        wrongCount = []

        while True:
            clr()

            if len(tested) == len(words):
                allt = round(allt,2)

                print("Congrats! You have answered all the questions!\n")
                print("Time used: " + str(allt))
                print("Accuracy: " + str(round((1-len(wrongCount)/len(words))*100,1)) + "%")
                print("Average time used for each word: " + str(round(allt/len(words),2)))
                print("Average rating: " + str(round(np.mean(ratings),1)) + "\n")
                input()
                break

            while True:
                word = words.sample(1).iloc[0]
                if word.name not in tested:
                    break

            print(f"{count}/{len(words)}")

            print(word["Chi"]+" ("+word["POS"]+")")

            if not config["blindMode"]:
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
                    allt += timeused
                    print("\nCorrect!")
                    print(f"Used {timeused: .2f} seconds")
                    rt = round(min(10.0,10*(len(word["Eng"])/timeused)/config["tpSpeed"]),1)
                    print("Rating: " + str(rt) + "/10.0")
                    ratings.append(rt)
                    count += 1
                    input()
                else:
                    print("\nWrong!")
                    if config["showAns"]:
                        print("\nCorrect answer: " + word["Eng"])
                    if word.name not in wrongCount:
                        wrongCount.append(word.name)
                    input()

            else:
                break


    elif mode == "2":
        while True:
            clr()

            eng = input("English word: ")
            chi = input("Chinese meaning: ")
            pos = input("Part of speech: ")

            if eng == "" or chi == "" or pos == "":
                break

            words = pd.concat([words.reset_index(drop=True),pd.DataFrame({"Eng": [eng], "Chi": [chi], "POS": [pos]}).reset_index(drop=True)],axis=0,ignore_index=True).drop(words.filter(like="Unnamed").columns,axis=1)
            words.to_csv("words.csv",index=False)

            print("Inserted successfully!")
            input()

    elif mode == "3":
        while True:
            clr()

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
        clr()

        print("\n"*3)
        print(words)
        print("\n"*3)
        input()

    elif mode == "5":
        while True:
            clr()
            print("Settings:\n\n1.Typing speed to get max rating:",config["tpSpeed"],"letters/s\n2.Blind mode:","On" if config["blindMode"] else "Off","\n3.Show correct answer after getting wrong:","On" if config["showAns"] else "Off","\n")

            choice = input("The setting you want to modify: ")
            if choice == "1":
                ts = input("\nNew typing speed: ")

                try:
                    ts = round(float(ts),1)
                    if ts > 0:
                        config["tpSpeed"] = ts
                        print("\nModified successfully")
                        input()
                    else:
                        print("\nValue must be positive")
                        input()
                except:
                    print("\nValue invalid")
                    input()

            elif choice == "2":
                print("\n1.Turn on blind mode\n2.Turn off blind mode\n")
                bm = input("Your choice: ")

                if bm == "1":
                    config["blindMode"] = True
                    print("\nBlind mode turned on successfully")
                    input()
                elif bm == "2":
                    config["blindMode"] = False
                    print("\nBlind mode turned off successfully")
                    input()
                else:
                    print("\nInput invalid")
                    input()

            elif choice == "3":

                print("\n1.Turn on show answer\n2.Turn off show answer\n")
                bm = input("Your choice: ")

                if bm == "1":
                    config["showAns"] = True
                    print("\nShow answer turned on successfully")
                    input()
                elif bm == "2":
                    config["showAns"] = False
                    print("\nShow answer turned off successfully")
                    input()
                else:
                    print("\nInput invalid")
                    input()

            else:
                break


    elif mode == "&&--&&":
        for i in range(300):
            words = pd.concat([words,pd.DataFrame({"Eng": ["banana"],"Chi": ["香蕉"], "POS": ["n."]})]).reset_index(drop=True)
            print("Added new datum")
            time.sleep(0.1)

    else:

        with open("config.json","w") as file:
            json.dump(config,file)

        exit()
