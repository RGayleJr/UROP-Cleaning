import pandas as pd
import numpy as np
import DataCleaningFunctions as dcf

filename= 'olympics.csv'

df = pd.read_csv(filename, header= 1)
print(df.head())
dcf.initiate(df)
dcf.rename_cols(df, 
{
    'Unnamed: 0': 'Country',
    '? Summer': 'Summer',
    '01 !': 'Gold',
    '02 !': 'Silver',
    '03 !': 'Bronze',
    '? Winter': 'Winter',
    '01 !.1': 'Gold.1',
    '02 !.1': 'Silver.1',
    '03 !.1': 'Bronze.1',
    '? Games': 'Games',
    '01 !.2': 'Gold.2',
    '02 !.2': 'Silver.2',
    '03 !.2': 'Bronze.2'
})
dcf.initiate(df)
dcf.split_at_char(df, 'Country', ' ', 'Country Code')
dcf.create_limiting_factor(df, 'Country Code', 'letters')
dcf.remove_cols(df, 'Country')
dcf.remove_row_containing(df, 'Total.1', 0)
dcf.reset_index(df)
dcf.only_keep_cols(df, ['Country Code', 'Summer', 'Winter', 'Games', 'Combined total'])
dcf.make_col_index(df, 'Country Code')
dcf.subtract_num(df, 'Combined total', 10)

print(df.head())