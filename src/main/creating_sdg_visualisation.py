import json
from lib2to3.pgen2.token import RARROW
from bson import json_util
import json
import os
import math
import csv
import time
import sys
import pandas as pd
import plotly.express as px

import pymongo 


def sdgVisualisation(request):
    """
        Returns the render for the IHE Visualisation page
    """

    # Get the visualisation data from MongoDB
    client = pymongo.MongoClient(get_details('MONGO_DB', 'client'))
    col1 = client.Scopus.SDGFaculty
    data1 = col1.find()
    """
    faculty         sdg1                                    sdg2        sdg3    ....
    Engineering     [15, AMERC001, ...X15,... SECU0009]
    social sciences
    ...
    """
    col2 = client.Scopus.studentspermodule
    data2 = col2.find()
    """
    moduleID        numberofstudents        lastupdated
    AMERC001        150                         "time"
    ...
    """
    jsonfaculty = json.loads(json_util.dumps(data1)) # process mongodb response to a workable dictionary format       
    """
    {"faculty": "engineering", "sdg1" : [15, "AMERC001",...,"SECU0009"], ...}
    {"faculty" : "social sciences", "sdg1" : [10, "AMERC0123",...,"COMP0131"],...}
    """

    dataframeforsdg1 = {'faculties' : list(jsonfaculty.get('faculty')),
                    'number of modules' : list(jsonfaculty.get('sdg1')
                    }
    df1 = pd.DataFrame(dataframeforsdg1)
    """
            faculties   number of modules
        0    engineering       15
        1    social sciences   10
        2    ..                ...
        3    ..                ...
        4    ..                ...
    """
    fig1 = px.bar(df1, y="Number of Modules", x="Faculties")
    #print(dataframeforsdg1)
    df1 = df1.reset_index()

    for index, row in df1.iterrows():
        fig.add_annotation(
            {
                "x": row["Faculties"],
                "y": row["Number of Modules"],
                "text": f"""<a href="{put whatever hyperlink}" target="_blank">{r[1]["faculties"]}</a>""",
            }
        )


    #---------------------------------------------------------------------------------------------------------------#

    jsonstudents = json.loads(json_util.dumps(data2)) # process mongodb response to a workable dictionary format
    """
    {"moduleID": "AMERC001", "numberofstudents" : 150, "lastupdated": time}
    """

    # Generate the context for IHE specific PyLDAvis and t-SNE visualisations
    # context = {
    #     "pylda": data['PyLDA_ihe'],
    #     "tsne": data['TSNE_ihe'],
    #     "segment": "iheVisualisation"
    # }


    client.close()
    return render(request, "ihe_model_vis.html", context)
