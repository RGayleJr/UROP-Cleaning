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

"""
** Means order does not matter **
Click 'PID'; in SPECIFIC COMMANDS choose create limiting factor and then choose digits
Click on cell ('PID', 1); in SPECIFIC COMMANDS choose change value and type in 100002000
Click 'ST_NAME'; in SPECIFIC COMMANDS choose create limiting factor and then choose letters
Click 'PID'; in In SPECIFIC COMMANDS choose 'Change Case' and choose 'Titlecase'
Click 'PID'; choose NONE/NaN to open drop down to choose 'Change' and type 'Unknown'
Click 'OWN_OCCUPIED'; type in search bar (3) 'TRUE'; click the arrow and choose "Replace with"; then type 'Y'
Click 'OWN_OCCUPIED'; type in search bar (3) 'FALSE'; click the arrow and choose "Replace with"; then type 'N'
Click on cell ('OWN_OCCUPIED', 3); in SPECIFIC COMMANDS choose change value and type 'Y'
Click on 'Unnamed: 4'; click 'Remove' (1) **
Click 'MOVE_IN_DATE'; type in search bar (3) '.'; click the arrow and choose "Replace with"; then type '/'
Click 'MOVE_IN_DATE'; type in search bar (3) '-'; click the arrow and choose "Replace with"; then type '/'
Click on cell ('MOVE_IN_DATE', 4); in SPECIFIC COMMANDS choose change value and type '03/02/2016'
Click on cell ('MOVE_IN_DATE', 5); click 'Remove' (1) **
Click 'NUM_BEDROOMS'; in SPECIFIC COMMANDS choose create limiting factor and then choose digits
Click 'NUM_BATH'; in SPECIFIC COMMANDS choose create limiting factor and then choose digits
Click 'SQ_FT'; in SPECIFIC COMMANDS choose create limiting factor and then choose digits

Click 'MOVE_IN_DATE'; click NONE/Nan, then from the drop down choose to keep rows
                OR
Click 'NONE/Nan' (4) and choose 'Remove rows'
"""