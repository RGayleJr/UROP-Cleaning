import pandas as pd
import numpy as np
import DataCleaningFunctions as dcf

filename= 'BL-Flickr-Images-Book.csv'

df = pd.read_csv(filename)

to_drop = [
    'Edition Statement', 'Corporate Author', 'Corporate Contributors',
    'Former owner', 'Engraver', 'Contributors', 'Issuance type', 'Shelfmarks'
]

to_keep = [
    'Identifier', 'Place of Publication', 'Date of Publication'
]

dcf.remove_cols(df, to_drop)
dcf.only_keep_cols(df, to_keep)
# print(dcf.is_every_value_unique(df, 'Identifier'))
# print(dcf.is_every_value_unique(df, 'Place of Publication'))
dcf.make_col_index(df, 'Identifier')
tempx = dcf.get_row(df, 206)
tempy = dcf.get_row_positional(df, 0)
# print(tempx)
# print(tempy)

dcf.create_limiting_factor(df, 'Date of Publication', 'digits', 4, True, 'start')
# extr = df['Date of Publication'].str.extract('^(\\d{4})', expand=False)
# df['Date of Publication'] = pd.to_numeric(extr)

# dcf.only_keep_cols(df, ['Place of Publication'], filename= filename)
dcf.boolean_db_contains(df, 'Place of Publication', 'London', 'In London?')
dcf.find_and_replace_cell_within_col(df, 'Place of Publication', 'London', 'London')
dcf.find_and_replace_cell_within_col(df, 'Place of Publication', 'Oxford', 'Oxford')
