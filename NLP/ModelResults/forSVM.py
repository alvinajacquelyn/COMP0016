import pyodbc
import datetime
import pandas as pd
import json
import os, sys


# SERVER LOGIN DETAILS
server = 'miemie.database.windows.net'
database = 'MainDB'
username = 'miemie_login'
password = 'e_Paswrd?!'
driver = '{ODBC Driver 17 for SQL Server}'
curr_time = datetime.datetime.now()

# CONNECT TO DATABASE
myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
threshold = 20


def progress(count, total, custom_text, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '*' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s %s\r' %(bar, percents, '%', custom_text, suffix))
    sys.stdout.flush()

def getDescription(moduleID):
    cur = myConnection.cursor()
    cur.execute(
        "SELECT Description FROM ModuleData WHERE Module_ID = (?)", (moduleID))
    data = cur.fetchall()
    if len(data) == 0:
        return ""
    return data

def process():
    tempcwd = os.getcwd()
    results = pd.DataFrame(columns=['ModuleID', 'Description', 'SDG'])
    with open('../training_results.json') as json_file:
        data = json.load(json_file)
        perplexity = data['Perplexity']
        docTopics = data['Document Topics']
        finalData = {}
        counter = 0
        for module in docTopics:
            progress(counter, len(docTopics), "Forming SVM dataset")
            if counter < 10:
                weights = docTopics[module]
                w = []
                for i in range(len(weights)):
                    weights[i] = weights[i].replace('(', '').replace(')', '').replace('%', '').replace(' ', '').split(',')
                    sdgNum = weights[i][0]
                    weightSDG = weights[i][1]
                    try:
                        weightSDG = float(weightSDG)
                    except:
                        weightSDG = 0.0
                    w.append(weightSDG)

                m = max(w)
                if m >= threshold:
                    rowDataFrame = pd.DataFrame([[module, getDescription(module)[0][0], m]], columns=results.columns)
                else:
                    rowDataFrame = pd.DataFrame([[module, getDescription(module)[0][0], None]], columns=results.columns)
                results = results.append(rowDataFrame, verify_integrity=True, ignore_index=True)
            counter += 1
    print()
    return results

data = process()
data.to_pickle("SVM_dataset")
