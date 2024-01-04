import requests
import json
from parsel import Selector
import pandas as pd
import csv

def table_scrape(_start, _end, data_dict):
    begin = _start
    end = _end

    URL = f"https://barttorvik.com/team-tables_each.php?tvalue=All&year=2024&sort=&t2value=None&oppType=All&conlimit=All&begin={begin}&end={end}&top=0&quad=4&mingames=0&toprk=0&venue=All&type=All&yax=3"
    r = requests.get(URL)

    # get columns
    sel = Selector(text=r.text)
    script = sel.xpath("//script[contains(., 'statnames')]/text()")

    names = script.re("statnames\[(\d+)\]='([^']+)';")
    heads = [""] * int((len(names) / 2))

    for i in range(0, len(names), 2):
        heads[int(names[i])] = str(names[i + 1]).replace(" ", "_")

    heads = ["ID"] + heads
    heads.insert(7, "Losses")

    # get data
    sel = Selector(text=r.text)
    script = sel.xpath("//script[contains(., 'var gdata')]/text()")

    data = script.re("var gdata = (.+?);")[0]
    data = json.loads(data)

    df = pd.DataFrame(columns=heads)

    for d in data:
        team = d[0]
        if team in data_dict: 
            id = data_dict.get(team)
            d.insert(0, id)

            if d[6] == None:
                d[6] = 0

            if d[7] == None:
                d[7] = 0

            losses = int(d[7]) - int(d[6])

            d.insert(7, losses)
            
            df.loc[len(df)] = d



    df.drop(
        columns=["PAKE", "PASE", "Talent", "WAB", "Avg_Hgt.", "Eff._Hgt.", "Exp.", "Year", "Record"],
        inplace=True,
    )

    return df
