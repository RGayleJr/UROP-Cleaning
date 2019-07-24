import pandas as pd
import numpy as np
import DataCleaningFunctions as dcf

filename = 'MiniDB.csv'

df = pd.read_csv(filename, names= ['Name', 'Surname', 'Street', 'City', 'State', 'Zipcode'])
print(df.head())

dcf.initiate(df)
dcf.remove_rows_with_nonenan(df)
dcf.remove_whatever(df, 'Name', '".*"')
dcf.remove_whitespace(df, 'Name')
dcf.make_titlecase(df, 'Street')
dcf.make_titlecase(df, 'City')
dcf.make_uppercase(df, 'State')
dcf.combine_cols(df, 'Street', 'City')
dcf.combine_cols(df, 'Street', 'State')
dcf.combine_cols(df, 'Street', 'Zipcode')
dcf.rename_cols(df, {'Street': 'Address'})
dcf.infer_datatype_value(df, 'Address')
dcf.change_value(df, 'Name', 2, 'John(R.)')
dcf.combine_cols(df, 'Name', 'Surname')
dcf.make_col_index(df, 'Name')

print(df.head())