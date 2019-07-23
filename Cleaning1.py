import pandas as pd
import numpy as np
import pdb
import DataCleaningFunctions as dcf

filename= 'BL-Flickr-Images-Book.csv'

df = pd.read_csv(filename)

to_drop = [
    'Edition Statement', 'Corporate Contributors', 'Corporate Author',
    'Contributors', 'Issuance type'
]

to_keep = [
    'Identifier', 'Place of Publication', 'Date of Publication',
    'Shelfmarks'
]

dcf.initiate(df)
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

dcf.boolean_db_contains(df, 'Place of Publication', 'London', 'In London?')
dcf.find_and_replace_cell_within_col(df, 'Place of Publication', 'London', 'London')
dcf.find_and_replace_cell_within_col(df, 'Place of Publication', 'Oxford', 'Oxford')
# # dcf.split_at_char(df, 'Place of Publication', 'n', 'Pt 2')
# # dcf.remove_row(df, 216)
dcf.remove_row_containing(df, 'Place of Publication', 'London')
dcf.split_at_char(df, 'Shelfmarks', 'HMNTS', 'ID #')
# # dcf.remove_cols(df, 'In London?')
dcf.remove_cols(df, 'Shelfmarks')
dcf.split_at_char(df, 'ID #', '.', 'temp')
dcf.split_at_char(df, 'temp', '.', '#2')
dcf.remove_cols(df, 'temp')
dcf.create_limiting_factor(df, 'ID #', 'digits')
dcf.create_limiting_factor(df, '#2', 'digits')
dcf.combine_cols(df, 'ID #', '#2')
dcf.apply_func_to_col(df, lambda x: x - 1, 'ID #')
dcf.sort_by_col(df, 'Place of Publication')