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
print(df.head())


dcf.initiate(df)
dcf.sort_by_col(df, 'RegionName')
dcf.combine_cols(df, 'State', 'RegionName')
dcf.split_at_char(df, 'State', ' ', 'Region')
dcf.change_col_type(df, 'State', 'Numbers')
dcf.remove_row_containing(df, 'State', 'Ohio')
dcf.remove_duplicate_rows(df)
dcf.rename_cols(df, {'Region': 'Area'})
dcf.infer_datatype_value(df, 'Area')
dcf.reset_index(df)
dcf.create_limiting_factor(df, 'State', 'letters', 3, True, 'start')

print(df.head())
