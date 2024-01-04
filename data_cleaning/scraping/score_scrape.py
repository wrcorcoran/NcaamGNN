import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By 
import time
import re

def query(year, conference, driver):
    URL = f"https://barttorvik.com/gamestat.php?sIndex=0&year={year}&tvalue=All&cvalue={conference}&opcvalue=All&ovalue=All&minwin=All&mindate=&maxdate=&typev=All&venvalue=All&minadjo=0&minadjd=200&mintempo=0&minppp=0&minefg=0&mintov=200&minreb=0&minftr=0&minpppd=200&minefgd=200&mintovd=0&minrebd=200&minftrd=200&mings=0&mingscript=-100&maxx=2500&coach=All&opcoach=All&adjoSelect=min&adjdSelect=max&tempoSelect=min&pppSelect=min&efgSelect=min&tovSelect=max&rebSelect=min&ftrSelect=min&pppdSelect=max&efgdSelect=max&tovdSelect=min&rebdSelect=max&ftrdSelect=max&gscriptSelect=min&sortToggle=1"

    driver.get(URL)

    time.sleep(5)

    data = driver.find_elements(By.XPATH, '//*[@id="tble"]/table/tbody')

    return data[0].text

def transform_date(input_string):
    date_object = datetime.strptime(input_string, "%m/%d/%y")
    return date_object.strftime("%Y%m%d")


def transform_score(input_string):
    scores = input_string.split("-")
    result = scores[0][0]
    scores[0] = scores[0][1:]

    if result == "W":
        return int(scores[0]) - int(scores[1])
    else:
        return int(scores[1]) - int(scores[0])

def string_to_df(s, conferences):
    locations = ['H', 'A', 'N']

    split_str = s.split('\n')
    split_str = split_str[1:]

    labels = split_str[0]
    labels = labels.replace("ADJ. O", "ADJ.O")
    labels = labels.replace("ADJ. D", "ADJ.D")
    labels = labels.split()
    split_str = split_str[1:]
    split_str.pop()

    df = pd.DataFrame(columns=labels)

    for s in split_str:
        s = re.sub(r', ', '', s)
        s = s.split()

        if (len(s) != len(labels)):
            temp_array = s[0:4]

            i = 4
            first = ""
            while (s[i] not in conferences):
                if (s[i + 1] not in conferences):
                    first += s[i] + " "
                else:
                    first += s[i]
                    temp_array.append(first)
                
                i += 1
            
            temp_array.append(s[i])
            i += 1
            
            second = ""
            while (s[i] not in locations):
                if (s[i + 1] not in locations):
                    second += s[i] + " "
                else:
                    second += s[i]
                    temp_array.append(second)

                i += 1

            temp_array.extend(s[i:len(s)])
            df.loc[len(df)] = temp_array

        else:
            df.loc[len(df)] = s

    df["DATE"] = df["DATE"].apply(transform_date)
    df["RESULT"] = df["RESULT"].apply(transform_score)
    df = df[["DATE", "TEAM", "OPP.", "VENUE", "RESULT"]]

    return df