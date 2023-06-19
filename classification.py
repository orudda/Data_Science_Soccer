import os
import json
import pandas as pd

class Cla:
    def __init__(self):
        self.df_spadl = self.loadData('files/spadl.json')
    
    def loadData(self, dataname):
        path = os.path.join(dataname)
        with open(path) as f:
            data = json.load(f)

        return pd.DataFrame(data)