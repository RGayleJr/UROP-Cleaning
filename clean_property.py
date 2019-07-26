import pandas as pd
import numpy as np
import DataCleaningFunctions as dcf
import pdb

filename = 'property.csv'

df = pd.read_csv(filename)
print('The original DF')
print(df)

dcf.initiate(df)
dcf.create_limiting_factor(df, 'PID', 'digits')
dcf.change_value(df, 'PID', 1, 100002000)
dcf.create_limiting_factor(df, 'ST_NAME', 'letters')
dcf.make_titlecase(df, 'ST_NAME')
dcf.change_nonenan_within_col(df, 'OWN_OCCUPIED', 'Unkown')
dcf.find_and_replace_cell_within_col(df, 'OWN_OCCUPIED', 'TRUE', 'Y')
dcf.find_and_replace_cell_within_col(df, 'OWN_OCCUPIED', 'FALSE', 'N')
dcf.change_value(df, 'OWN_OCCUPIED', 3, 'Y')
dcf.remove_cols(df, 'Unnamed: 4')
dcf.find_and_replace_within_col(df, 'MOVE_IN_DATE', '.', '/')
dcf.find_and_replace_within_col(df, 'MOVE_IN_DATE', '-', '/')
dcf.change_value(df, 'MOVE_IN_DATE', 4, '03/02/2016')
dcf.remove_value(df, 'MOVE_IN_DATE', 5)
dcf.create_limiting_factor(df, 'NUM_BEDROOMS', 'digits')
dcf.create_limiting_factor(df, 'NUM_BATH', 'digits')
dcf.create_limiting_factor(df, 'SQ_FT', 'digits')

print('The cleaned DF')
print(df)

x = df.copy()
dcf.keep_rows_with_nonenan_within_col(df, 'MOVE_IN_DATE')

print('The houses still for sale (with no move in date)')
print(df)

dcf.remove_rows_with_nonenan(x)
print('The DF with only houses with all IMPORTANT information filled out')
print(x)