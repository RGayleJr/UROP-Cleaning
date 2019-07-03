import pandas as pd
import numpy as np
import pdb

def remove_cols(df, remove):
    """
    'df' is the dataframe and 'remove' is a list of col heads to be removed
    """
    df.drop(columns= remove, inplace= True)

def remove_row(df, remove):
    """
    'df' is the dataframe and 'remove' is a list of rows to be removed
    """
    df.drop(index= remove, inplace= True)

def only_keep_rows(df, keep):
    """
    'df' is the dataframe and 'keep' is a list of rows to keep
    """
    remove = []
    keep_set = set(keep)

    #find every col that is not being kept and add to the list 'remove'
    for row in df.index:
        if row not in keep_set:
            remove.append(row)
    
    #drop the cols not being kept
    df.drop(index= remove, inplace= True)

def remove_duplicate_rows(df):
    """
    'df' is the dataframe
    """
    df.drop_duplicates()

def only_keep_cols(df, keep):
    """
    'df' is the dataframe and 'keep' is a list of col heads to keep
    """
    remove = []
    keep_set = set(keep)

    #find every col that is not being kept and add to the list 'remove'
    for col in df.columns:
        if col not in keep_set:
            remove.append(col)
    
    #drop the cols not being kept
    df.drop(columns= remove, inplace= True)

def is_every_value_unique(df, colname):
    """
    'df' is the dataframe and colname is a col name
    """
    return df[colname].is_unique

def make_col_index(df, colname):
    """
    'df' is the dataframe and colname is a col name
    """
    #A Pandas Index doesn’t make any guarantee of being unique
    if not is_every_value_unique(df, colname):
        print("Not every index is unique")
    df.set_index(colname, inplace= True)

def get_row(df, num):
    """
    'df' is the dataframe and 'num' is the index (according to left-most col)
    """
    return df.loc[num]

def get_row_positional(df, num):
    """
    'df' is the datagrame and 'num' is the index (according to position)
    """
    return df.iloc[num]

def get_col(df, col):
    """
    'df' is the dataframe and 'col' is the column name
    """
    return df[col]

def create_limiting_factor(df, colname, characters, len= 0, exact= False, position= None):
    """
    'df' is the dataframe; 'characters' is "alphanumeric", "digits",
    "non-digits"; 'len' is a number for the desired length; 'exact'
    is "True" if the desired length is exact and "False" if it is
    a minimum; 'position' is "start" or "end"
    """
    final = ''
    if position == 'start':
        final = final + '^'
    elif position == 'end':
        final = final + '$'

    if characters == 'digits':
        final = final + '(\\d'
    elif characters == 'non-digits':
        final = final + '(\\D'
    elif characters == 'alphanumeric':
        final = final + '(\\w'
    
    if len != 0:
        final = final + '{' + str(len)
        if exact == False:
            final = final + '+'
        final = final + '}'
        
    final = final + ')'
    
    extr = df[colname].str.extract(final, expand= False)
    df[colname] = pd.to_numeric(extr)

def boolean_db_contains(df, colname, string, newcolname= None):
    """
    Creates a column that expresses whether or not a substring is within
    each cell for a certain column.
    'df' is the dataframe; 'colname' is the column name to check; 'string' is
    the substring to search for; 'newcolname' is the name of the column that
    the boolean values should have
    """
    ex = df[colname].str.contains(string)
    if newcolname == None:
        newcolname = 'Contains ' + string
    df.insert(df.columns.get_loc(colname) + 1, newcolname, list(ex), True)

def find_and_replace_cell_within_col(df, colname, str1,str2):
    """
    Searches for 'str1' within a column and replaces
    the cell's text with 'str2'
    """
    temp = df[colname]
    conditional = temp.str.contains(str1)
    # pdb.set_trace()
    df[colname] = np.where(conditional, str2, temp.str.replace('', ''))

def find_and_replace_cell_everywhere(df, str1, str2):
    """
    Does the same thing as find_and_replace_within_col, but
    for every column
    """
    columns = list(df)

    for i in columns:
        find_and_replace_cell_within_col(df, i, str1, str2)

def find_and_replace(df, str1, str2):
    """
    Finds and replaces 'str1' with 'str2'
    """
    df.replace(str1, str2, inplace= True)

def change_header_row(filename, rownum):
    """
    Sets the header row to the 'rownum' row index
    """
    df = pd.read_csv(filename, header= rownum)

def rename_cols(df, new_names):
    """
    Changes name of column headers.
    'new_names' is a list of the new names, in order; 'df' is 
    the dataframe
    """
    old_names = list(df)
    mapping = {}
    limiter = len(new_names)
    if len(old_names) < len(new_names):
        limiter = len(old_names)
    for i in range(limiter):
        mapping[old_names[i]] = new_names[i]

    df.rename(columns= mapping, inplace= True)

def reset_index(df):
    """
    Resets index
    'df' is the dataframe
    """
    df.reset_index(drop= True)