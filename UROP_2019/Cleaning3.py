import pandas as pd
import numpy as np
import DataCleaningFunctions as dcf

filename= 'olympics.csv'

df = pd.read_csv(filename, header= 1)

# dcf.change_header_row(filename, 1)

new_names = [
    'Country', 'Summer Olympics', 'Gold', 'Silver', 'Bronze', 
    'Total', 'Winter Olympics', 'Gold.1', 'Silver.1', 'Bronze.1',
    'Total.1', '# Games', 'Gold.2', 'Silver.2', 'Bronze.2'
]

dcf.rename_cols(df, new_names)