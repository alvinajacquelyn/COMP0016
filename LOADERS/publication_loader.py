import pymongo
import json
from LOADERS.loader import Loader

class PublicationLoader(Loader):
    def load(self, count):
        client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.hw8fo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.Scopus
        col = db.Data
        data = col.find()
        return data