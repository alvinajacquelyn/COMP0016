import psycopg2
import pyodbc
import sys
import pandas as pd


def getMySQL():
    # SERVER LOGIN DETAILS
    server = 'miemie.database.windows.net'
    database = 'MainDB'
    username = 'miemie_login'
    password = 'e_Paswrd?!'
    driver = '{ODBC Driver 17 for SQL Server}'

    # CONNECT TO DATABASE
    myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server +
                                  ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return myConnection

def getPostgres_modules():
    con = psycopg2.connect(database='django_db_miemie_ucl', user='miemie_admin@miemiedjangoapp',
                           host='miemiedjangoapp.postgres.database.azure.com', password='e_Paswrd?!', port='5432')
    cur = con.cursor()
    cur.execute("""
        select  id
            ,"Department_Name"
            ,"Department_ID"
            ,"Module_Name"
            ,"Module_ID"
            ,"Faculty"
            ,"Module_Lead"
            ,"Catalogue_Link"
            ,"Description"
            ,"Credit_Value"
            ,"assignedSDG"
            from public."App_module"
    """)
    result = cur.fetchall()
    return result

def pushToSQL(module_id: str, data: list) -> None:
    if len(data) != 0:
        connection = getMySQL()
        cur = connection.cursor()
        for i in data:
            insertion = "INSERT INTO TestModAssign (Module_ID, SDG) VALUES (?, ?)"
            cur.execute(insertion, (module_id, i))
        connection.commit()
        connection.close()

def clearTable() -> None:
    connection = getMySQL()
    cur = connection.cursor()

    command = "TRUNCATE TABLE TestModAssign"
    cur.execute(command)
    connection.commit()
    connection.close()

def progress(count: int, total: int, custom_text: str, suffix='') -> None:
    """
        Visualises progress for a process given a current count and a total count
    """

    bar_len = 60  # size of the progress bar on the commandline
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '*' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s %s\r' %(bar, percents, '%', custom_text, suffix))
    sys.stdout.flush()

def process_module_LDA_visualisation() -> None:
    clearTable()
    data = getPostgres_modules()
    counter = 1
    l = len(data)

    for mod in data:
        if mod:
            progress(counter, l, "Writing to TestModAssign")
            counter += 1
            module_result_accumulator = {}
            mod_id = mod[4]
            module_result_accumulator[mod_id] = []
            
            if mod[len(mod) - 1]:
                mod_prediction = mod[len(mod) - 1]['ModelResult'] # str with potential CSV

                if mod_prediction is not None and mod_prediction != None and len(mod_prediction) != 0:
                    if ',' in mod_prediction:
                        temp = mod_prediction.split(',')
                        for i in temp:
                            module_result_accumulator[mod_id].append(int(i))
                    else:
                        module_result_accumulator[mod_id].append(int(mod_prediction))
                pushToSQL(mod_id, module_result_accumulator[mod_id])
    print()


if __name__ == "__main__":
    process_module_LDA_visualisation()