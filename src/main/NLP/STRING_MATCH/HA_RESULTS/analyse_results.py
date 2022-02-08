import json
import pandas as pd

def open_file(file_name):
    with open(file_name) as f:
        return json.load(f)

def write_to_csv(data: list, cols: list, file_name) -> None:
    longest = 0
    for i in cols:
        if len(data[i]) > longest:
            longest = len(data[i])

    for i in cols:
        while len(data[i]) < longest:
            data[i].append("")

    df = pd.DataFrame(data)
    print(df)

    df.to_csv(file_name, encoding='utf-8', index=False)

def analyse(data: dict, titles: list) -> None:
    occurences = {}
    for i in titles:
        occurences[i] = []

    for doi, values in data.items():
        for ha in values:
            ha_occurence_len = len(values[ha])
            ha_number = int(ha.split(' ')[1])
            occurences[titles[ha_number - 1]].append(doi)
    return occurences

def run():
    print("Reading data...")
    data = open_file("main/NLP/STRING_MATCH/HA_RESULTS/scopus_ha_matches.json")
    titles = pd.read_csv("main/HA_KEYWORDS/HA_Keywords.csv")
    print("Analysing...")
    occurences = analyse(data, list(titles.columns))
    print("Saving...")
    write_to_csv(occurences, titles,"main/NLP/STRING_MATCH/HA_RESULTS/analyse_results.csv")

run()
# python3 main/NLP/STRING_MATCH/HS_RESULTS/analyse_results.py