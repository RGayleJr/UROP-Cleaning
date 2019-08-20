import pandas as pd
import numpy as np
import pdb
import re
import math

def is_nan(x):
        return (x is np.nan or x != x)

def get_col_name(df, col):
    columns = set(df)
    if col not in columns:
        if type(col) == int:
            colname = df.columns[col]
            return colname
        for i in columns:
            colname = i[0]
            if colname == col:
                return i
    else:
        return col

def get_col_list(df, cols):
    final = []
    for col in cols:
        temp = get_col_name(df, col)
        final.append(temp)
    return final

def initiate(df):
    # columns = list(df)

    # for i in columns:
    #     mapping[i] = Column()
        
    infer_datatype_values(df)  

def change_value(df, col, row, new_value):
    col = get_col_name(df, col)
    df.at[row, col] = new_value

def remove_value(df, col, row):
    col = get_col_name(df, col)
    change_value(df, col, row, np.nan)
    
def remove_cols(df, remove):
    """
    'df' is the dataframe and 'remove' is a list of col heads to be removed
    """
    if type(remove) == str or type(remove) == tuple:
        temp = []
        temp.append(remove)
        remove = temp

    final = get_col_list(df, remove)

    df.drop(columns= final, inplace= True)

def remove_rows(df, remove):
    """
    'df' is the dataframe and 'remove' is a list of rows to be removed
    """
    if type(remove) == str:
        temp = []
        temp.append(remove)
        remove = temp

    df.drop(index= remove, inplace= True)

    infer_datatype_values(df)
        
def only_keep_rows(df, keep):
    """
    'df' is the dataframe and 'keep' is a list of rows to keep or
    it is a tuple which represents a range (start, end)
    """
    remove = []
    if type(keep) == list:
        keep_set = set(keep)
    if type(keep) == tuple:
        keep = [i for i in range(keep[0], keep[1])]
        keep_set = set(keep)

    #find every col that is not being kept and add to the list 'remove'
    for row,_ in df.iterrows():
        if row not in keep_set:
            remove.append(row)
    
    #drop the cols not being kept
    remove_rows(df, remove)

    infer_datatype_values(df)

def remove_duplicate_rows(df):
    """
    'df' is the dataframe
    """
    size = len(df)
    df.drop_duplicates()
    new_size = len(df)
    diff = size - new_size
    if size == new_size:
        print('No Duplicates')
    else:
        print('Removed ' + diff + ' duplicates')
    infer_datatype_values(df)

def only_keep_cols(df, keep):
    """
    'df' is the dataframe and 'keep' is a list of col heads to keep
    """
    remove = []

    keep = get_col_list(df, keep)
    keep_set = set(keep)

    #find every col that is not being kept and add to the list 'remove'
    for col in df.columns:
        if col not in keep_set:
            remove.append(col)
    
    #drop the cols not being kept
    remove_cols(df, remove)   

def is_every_value_unique(df, colname):
    """
    'df' is the dataframe and colname is a col name
    """
    colname = get_col_name(df, colname)
    return df[colname].is_unique

def make_col_index(df, colname):
    """
    'df' is the dataframe and colname is a col name
    """
    #A Pandas Index doesn’t make any guarantee of being unique
    if not is_every_value_unique(df, colname):
        print("Not every index is unique. Not done")
        return
    colname = get_col_name(df, colname)
    df.set_index(colname, inplace= True)

def get_row(df, dna):
    """
    'df' is the dataframe and 'dna' is the index (according to left-most col)
    """
    return df.loc[dna]

def get_row_positional(df, num):
    """
    'df' is the datagrame and 'num' is the index (according to position)
    """
    return df.iloc[num]

def get_col(df, col):
    """
    'df' is the dataframe and 'col' is the column name
    """
    col = get_col_name(df, col)
    return df[col]

def get_value(df, col, row):
    col = get_col_name(df, col)
    return df.at[row, col]

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

    if characters == 'digits':
        final = final + '([\\d\\.]*[\\d]'
    elif characters == 'non-digits':
        final = final + '(\\D'
    elif characters == 'alphanumeric':
        final = final + '(\\w'
    elif characters == 'letters':
        final = final + '([A-Za-z]'
    
    if len != 0 and exact:
        final = final + '{' + str(len) + '}'
    if len != 0 and exact == False:
        final = final + str(len) + "+"
    if len == 0 and exact == False:
        final = final + '+'

    if position == 'end':
        final = final + '$'
        
    final = final + ')'
    
    colname = get_col_name(df, colname)
    
    extr = df[colname].str.extract(final, expand= False) 
    if characters == 'digits':
        df[colname] = pd.to_numeric(extr)
    else:
        df[colname] = extr
    infer_datatype_value(df, colname)

def boolean_db_contains(df, colname, string, newcolname= None):
    """
    Creates a column that expresses whether or not a substring is within
    each cell for a certain column.
    'df' is the dataframe; 'colname' is the column name to check; 'string' is
    the substring to search for; 'newcolname' is the name of the column that
    the boolean values should have
    """
    colname = get_col_name(df, colname)
    
    ex = df[colname].str.contains(string)

    if newcolname == None:
        newcolname = 'Contains ' + string
    df.insert(df.columns.get_loc(colname) + 1, newcolname, [str(i) for i in list(ex)], True)

    infer_datatype_value(df, newcolname)

def create_new_col(df, newcolname, position= None, value= np.nan):
    if position == None:
        position = len(list(df))
    df.insert(position, newcolname, [value for i in range(len(df))])

    infer_datatype_value(df, newcolname)

def remove_row_containing(df, colname, string):
    """
    Finds every row in column 'colname' that contains the str 'string'
    and removes it.
    'df' is the dataframe, 'colname' is the column name and 'string'
    is the str
    """
    colname = get_col_name(df, colname)

    ex = df[colname]
    ex_list = list(ex)
    temp = []
    for i in range(len(ex_list)):
        if type(string) == str:
            if string in ex_list[i]:
                temp.append(df.iloc[i].name)
        else:
            if string == ex_list[i]:
                temp.append(df.iloc[i].name)

    remove_rows(df, temp)

    infer_datatype_values(df)

    # df[~df[colname].isin([string])]

def keep_row_containing(df, colname, string):
    colname = get_col_name(df, colname)

    ex = df[colname]
    ex_list = list(ex)
    temp = []
    for i in range(len(ex_list)):
        if type(string) == str:
            if string not in ex_list[i]:
                temp.append(df.iloc[i].name)
        else:
            if string != ex_list[i]:
                temp.append(df.iloc[i].name)

        remove_rows(df, temp)

        infer_datatype_values(df)    

def change_nonenan_within_col(df, col, new_value):
    rows = list(df.index)
    col = get_col_name(df, col)

    for row in rows:
        if get_value(df, col, row) == None or is_nan(get_value(df, col, row)):
            change_value(df, col, row, new_value)

def change_nonenan(df, new_value):
    columns = list(df)
    for i in columns:
        change_nonenan_within_col(df, i, new_value)

def keep_rows_with_nonenan_within_col(df, col):
    rows = list(df.index)
    remove = set(rows)
    
    for row in rows:
        if get_value(df, col, row) == None or is_nan(get_value(df, col, row)):
            remove.remove(row)

    remove = list(remove)
    remove_rows(df, remove)

def remove_rows_with_nonenan_wihtin_col(df, col):
    rows = list(df.index)
    remove = []
    
    for row in rows:
        if get_value(df, col, row) == None or is_nan(get_value(df, col, row)):
            remove.append(row)

    remove_rows(df, remove)

def remove_rows_with_nonenan(df):
    columns = list(df)
    for i in columns:
        remove_rows_with_nonenan_wihtin_col(df, i)

def split_at_char(df, colname, string, newcolname):
    """
    Splits the column 'colname' into two at 'string'. ('string'
    not included)
    'df' is the Dataframe, 'colname' is the column to search for
    the str 'string', 'string' is where the column gets split, and
    'newcolname' is the name the new column will have
    """
    colname = get_col_name(df, colname)

    ex = df[colname]
    ex_list = list(ex)
    new_list = [None for i in range(len(ex_list))]
    
    for i in range(len(ex_list)):
        if string in ex_list[i]:
            word = ex_list[i]
            index = word.find(string)
            df.at[df.iloc[i].name, colname] = word[:index]
            new_list[i] = word[index + len(string):]

    df.insert(df.columns.get_loc(colname) + 1, newcolname, new_list, True)

    infer_datatype_value(df, colname)
    infer_datatype_value(df, newcolname)

def find_and_replace_cell_within_col(df, colname, str1,str2):
    """
    Searches for 'str1' within a column and replaces
    the cell's text with 'str2'
    """
    colname = get_col_name(df, colname)
    temp = df[colname]
    conditional = temp.str.contains(str1)
    df[colname] = np.where(conditional, str2, temp.str.replace('', ''))
    infer_datatype_value(df, colname)

def find_and_replace_cell_everywhere(df, str1, str2):
    """
    Does the same thing as find_and_replace_within_col, but
    for every column
    """
    columns = list(df)

    for i in columns:
        find_and_replace_cell_within_col(df, i, str1, str2)

    infer_datatype_values(df)

def find_and_replace(df, str1, str2):
    """
    Finds and replaces 'str1' with 'str2'
    """
    df.replace(str1, str2, inplace= True)

    infer_datatype_values(df)

def find_and_replace_within_col(df, col, str1, str2):
    col = get_col_name(df, col)

    df[col] = df[col].str.replace(str1, str2)

def change_header_row(df, filename, rownum):
    """
    Sets the header row to the 'rownum' row index
    """
    df = pd.read_csv(filename, header= rownum)

def rename_cols(df, new_names):
    """
    Changes name of column headers.
    'new_names' is a list or dict of the new names, in order; 'df' is 
    the dataframe
    """
    if type(new_names) == list:
        old_names = list(df)
        mapping = {}
        limiter = len(new_names)
        if len(old_names) < len(new_names):
            limiter = len(old_names)
        for i in range(limiter):
            mapping[old_names[i]] = new_names[i]
    if type(new_names) == dict:
        columns = list(df)
        temp = {}
        for name in new_names:
            if name not in columns:
                for i in columns:
                    col = i[0]
                    if col == name:
                        temp[i] = new_names[name]
                        break
            else:
                temp[name] = new_names[name]
        new_names = temp
        mapping = new_names
    df.rename(columns= mapping, inplace= True)

def reset_index(df):
    """
    Resets index
    'df' is the dataframe
    """
    df.reset_index(drop= True, inplace= True)

def combine_cols(df, col1, col2):

    """
    Combines two columns, 'col2' gets merged with 'col1' while
    'col2' gets deleted
    'df' is a Dataframe, 'col1' is the name of the column that
    changes, and 'col2' is the name of the column that merges
    """
    col1 = get_col_name(df, col1)
    col2 = get_col_name(df, col2)

    ex1 = df[col1]
    ex2 = df[col2]
    ex1_list = list(ex1)
    ex2_list = list(ex2)

    final = []
    tester = type(ex1_list[0])
    if type(ex1_list[0]) == type(ex2_list[0]):
        for i in range(len(ex1_list)):
            if tester != str:
                temp = ex1_list[i] + ex2_list[i]
                final.append(temp)
            else:
                temp = ex1_list[i] + ' ' + ex2_list[i]
                final.append(temp)
    else:
        for i in range(len(ex1_list)):
            temp = str(ex1_list[i]) + ' ' + str(ex2_list[i])
            final.append(temp)
    
    df[col1] = final

    remove_cols(df, col2)

    infer_datatype_value(df, col1)

# def enumerate_regex(selection):
    final = []

    def find_possibiliities(select):
        if len(select) == 0:
            return final
        
        if type(select[0]) == str:
            temp = select[0]
            if temp.isalpha():
                options = [temp, '[a-zA-Z]', ]

        for expr in final:
            for option in options:
                add(option, expr)

        find_possibiliities(select[1:])

    def add(option, exp):
        expression = exp[0]
        prev = exp[1]
        if option == prev and '+' !=  expression[-1] and '*' != expression[-1]:
            expr1 = expression.copy()
            expr2 = expression.copy()
            expr1.append('+')
            expr2.append('*')
            final.append((expr1, prev))
            final.append((expr2, prev))
        expr3 = expression.copy()
        expr3.append(option)
        final.append((expr3, option))
        
def infer_datatype_value(df, col):
    if "#LOCKED#" in col[1]:
        return

    col = get_col_name(df, col)

    sample_len = len(df)
    if len(df) > 10000:
        sample_len = round(.1 * len(df))
    hist = {}
    
    def is_nan(x):
        return (x is np.nan or x != x)

    for i in range(sample_len):
        key = type(df.iloc[i][col])
        data = df.iloc[i][col]
        if data == None or is_nan(data):
            continue
        elif key == str:
            if re.search('^[(]?\d{3}[\-)]? ?\d{3}[- ]?\d{4}$', data) != None:
                key = 'Phone Number'
            elif re.search('^\d{1,4}([-\/]\d{1,4}){1,2}$', data) != None:
                #^\d\d?[-/]\d\d?[-/]\d\d\d?\d?$
                key = 'Date'
            elif re.search('^\d*:\d+[\d:]*', data) != None:
                key = 'Time'
            elif re.search('^[A-Z a-z]+$', data) != None:
                key = 'Words'
            elif re.search('^\d+$', data) != None:
                key = 'Numbers'
            elif re.search('^\w+', data) != None:
                key = 'Alphanumeric'
            else:
                key = 'Misc'
        elif key == int or key == np.int64 or key == float or key == np.float64:
            key = 'Numbers'
        if key not in hist:
            hist[key] = 0
        hist[key] += 1

    final = None
    count = -1
    for entry in hist:
        if hist[entry] > count:
            final = entry
            count = hist[entry]

    if final == None:
        final = 'Unknown'

    if type(col) != tuple:    
        rename_cols(df, {col: (col, final)})
    else:
        rename_cols(df, {col: (col[0], final)})
    # mapping[col].type = final

def infer_datatype_values(df):
    columns = list(df)

    for i in columns:
        infer_datatype_value(df, i)

def change_col_type(df, col, new_type):

    col = get_col_name(df, col)
    if type(col) == tuple:
        rename_cols(df, {col: (col[0], new_type + " #LOCKED#")})
    else:
        rename_cols(df, {col: (col, new_type + ' #LOCKED#')})

def unlock_col_type(df, col):
    ogtype = col[1].replace(' #LOCKED#', '')
    rename_cols(df, {col: (col[0], ogtype)})

def sort_by_col(df, cols, ascend= True, Nan= 'last'):
    """
    'df' is the Dataframe. 'cols' is/are the column/s being sorted
    in order of importance. 'ascend' is True by default, and can be
    'False'. 'Nan' is where None values go by default, can be 'first'
    """
    if type(cols) == str:
        temp = []
        temp.append(cols)
        cols = temp

    final = get_col_list(df, cols)

    df.sort_values(by= final, ascending= ascend, na_position= Nan, inplace= True)

def apply_func_to_col(df, func, col):
    col = get_col_name(df, col)

    df[col] = df[col].apply(func)

def make_lowercase(df, col):
    apply_func_to_col(df, lambda x: x.lower(), col)

def make_uppercase(df, col):
    apply_func_to_col(df, lambda x: x.upper(), col)

def make_titlecase(df, col):
    apply_func_to_col(df, lambda x: x.title(), col)

def subtract_num(df, col, n):
    apply_func_to_col(df, lambda x: x - n, col)

def add_num(df, col, n):
    apply_func_to_col(df, lambda x: x + n, col)

def multiply_num(df, col, n):
    apply_func_to_col(df, lambda x: x * n, col)

def divide_num(df, col, n):
    apply_func_to_col(df, lambda x: x / n, col)

def clean_divide_num(df, col, n):
    apply_func_to_col(df, lambda x: x // n, col)

def square_num(df, col):
    apply_func_to_col(df, lambda x: x**x, col)

def remove_numbers(df, col):
    col = get_col_name(df, col)
    df[col] = df[col].str.replace('\d+', '')

def remove_letters(df, col):
    col = get_col_name(df, col)
    df[col] = df[col].str.replace('[a-zA-Z]+', '')

def remove_whitespace(df, col):
    col = get_col_name(df, col)
    df[col] = df[col].str.replace('\s+', '')

def keep_letters(df, col):
    col = get_col_name(df, col)
    df[col] = df[col].str.replace('[^a-zA-Z]+', '')

def keep_numbers(df, col):
    col = get_col_name(df, col)
    df[col] = df[col].str.replace('[^\d]+', '')

def remove_whatever(df, col, pattern):
    col = get_col_name(df, col)
    df[col] = df[col].str.replace(pattern, '')

"""
We should make the identifier column a changable column as well.
Like, by default its "Digits" and ascending, but we can change it 
to descending. If they change it to "Words" then it goes in
ascending order "abcdefg..."
I think it should like as much like Excel as possible. We want it
to be intuitive to use and people are already comfortable with
Excel. The suggestions format used in Trifacta seems the easiest
to use.
Pattern creator -- tool that alows the user to select as many
different selection of texts, and the computer will return
a reg ex that matches all of the selected texts.
Within column structures (if misc or alphanumerical, try
going more in depth (Title, (Numbers, Words, Date)) )
Options or things to do with things that do not match that type
    -remove them
    -set their values to something
Nest cols/rows
"""

"""
Is there code online for regex
Read paragraph again (Potter's Wheel)
Clean other datasets
Do a cleaning (describe function from pandas)
Design UI Mock-up
"""

"""
1. Make code to do things with col index
2. 