import pandas as pd
import numpy as np
import DataCleaningFunctions as dcf

filename= 'university_towns.txt'

university_towns = []

with open(filename) as file:
    for line in file:
        if '[edit]' in line:
            state = line
        else:
            university_towns.append((state, line))

df = pd.DataFrame(university_towns, columns= ['State', 'RegionName'])

def get_citystate(item):
    if ' (' in item:
        return item[:item.find(' (')]
    elif '[' in item:
        return item[:item.find('[')]
    else:
        return item

df = df.applymap(get_citystate)