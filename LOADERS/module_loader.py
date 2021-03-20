import pymongo
import json
import ssl
import os
import pandas as pd
import pickle
import pyodbc
from typing import Optional, Union

from bson import json_util
from LOADERS.loader import Loader

class ModuleLoader(Loader):
    def __init__(self):
        self.host = "mongodb+srv://admin:admin@cluster0.hw8fo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        self.data_file = "LOADERS/modules.pkl"
        self.prediction_path = "NLP/LDA/SDG_RESULTS/training_results.json"
        self.string_matches_path = "NLP/STRING_MATCH/SDG_RESULTS/module_matches.json"

    def get_modules_db(self, num_modules: Union[int, str]) -> pd.DataFrame:
        """
            Returns either all modules, or if specified, a number of modules
        """
        # SERVER LOGIN DETAILS
        server = 'miemie.database.windows.net'
        database = 'MainDB'
        username = 'miemie_login'
        password = 'e_Paswrd?!'
        driver = '{ODBC Driver 17 for SQL Server}'
        
        # CONNECT TO THE DATABASE
        myConnection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

        if num_modules == "MAX":
            # Load all modules.
            df = pd.read_sql_query("SELECT Module_Name, Module_ID, Description FROM [dbo].[ModuleData]", myConnection)
        else:
            # Load given number of modules.
            df = pd.read_sql_query("SELECT TOP (%d) Module_Name, Module_ID, Description FROM [dbo].[ModuleData]" % int(num_modules), myConnection)

        myConnection.commit()
        return df

    def load(self, count: int) -> pd.DataFrame:
        """
            Loads module data from pickled file.
            Returns Pandas DataFrame with columns: 'Module_ID' and 'Description'.
        """
        with open(self.data_file, "rb") as input_file:
            data = pickle.load(input_file)

        data = data.dropna()
        data = data.head(count) if isinstance(count, int) else data
        return pd.DataFrame(data=data, columns=["Module_ID", "Description"])

    def load_prediction_results(self):
        """
            Loads module SDG predictions from a serialised data file if exists, otherwise, loads MongoDB.
        """
        if os.path.exists(self.prediction_path):
            with open(self.prediction_path) as json_file:
                data = json.load(json_file)
        else:
            client = pymongo.MongoClient(self.host, ssl_cert_reqs=ssl.CERT_NONE)
            db = client.Scopus
            col = db.ModulePrediction
            data = col.find(batch_size=10)
            client.close()

        return data

    def load_string_matches_results(self):
        """
            Loads module SDG keyword string match results from serialised file, if it exists, otherwise from MongoDB
        """
        if os.path.exists(self.string_matches_path):
            with open(self.string_matches_path) as json_file:
                data = json.load(json_file)
        else:
            client = pymongo.MongoClient(self.host, ssl_cert_reqs=ssl.CERT_NONE)
            db = client.Scopus
            col = db.MatchedModules
            data = col.find(batch_size=10)
            client.close()

        return data
        
    def load_pymongo_db(self) -> None:
        """
            Downloads Module data from SQL Server and serialises it into <modules.pkl>
        """
        print("Loading modules from SQL server...")
        data = self.get_modules_db("MAX")
        with open(self.data_file, "wb") as output_file:
            pickle.dump(data, output_file)