import pandas as pd
import numpy as np
import pdb
import re
import math

# class Column:
#     def init(self):
#         self.type = None

# column_objects = []
# mapping = {}

def initiate(df):
    # columns = list(df)

    # for i in columns:
    #     mapping[i] = Column()
        
    infer_datatype_values(df)  

def remove_cols(df, remove):
    """
    'df' is the dataframe and 'remove' is a list of col heads to be removed
    """
    if type(remove) == str:
        temp = []
        temp.append(remove)
        remove = temp

    columns = list(df)
    final = []
    for each in remove:
        if each not in columns:
            for i in columns:
                col = i[0]
                if col == each:
                    final.append(i)
                    break
        else:
            final.append(each)

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
    'df' is the dataframe and 'keep' is a list of rows to keep
    """
    remove = []
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
    df.drop_duplicates()
    infer_datatype_values(df)

def only_keep_cols(df, keep):
    """
    'df' is the dataframe and 'keep' is a list of col heads to keep
    """
    columns = list(df)
    remove = []

    temp = set()
    for item in keep:
        if item not in columns:
            for i in columns:
                col = i[0]
                if col == item:
                    temp.add(i)
                    break
        else:
            temp.add(item)
    keep_set = temp

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
    try:
        return df[colname].is_unique
    except:
        columns = list(df)    
        for j in columns:
            col = j[0]
            if col == colname:
                return df[j].is_unique

def make_col_index(df, colname):
    """
    'df' is the dataframe and colname is a col name
    """
    #A Pandas Index doesn’t make any guarantee of being unique
    if not is_every_value_unique(df, colname):
        print("Not every index is unique")
    columns = list(df)
    if colname in columns:
        df.set_index(colname, inplace= True)
    else:
        for i in columns:
            col = i[0]
            if col == colname:
                df.set_index(i, inplace= True)

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
    columns = list(df)
    if col in columns:
        return df[col]
    else:
        for i in columns:
            colname = i[0]
            if col == colname:
                return df[i]

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
        final = final + '(\\d'
    elif characters == 'non-digits':
        final = final + '(\\D'
    elif characters == 'alphanumeric':
        final = final + '(\\w'
    
    if len != 0 and exact:
        final = final + '{' + str(len) + '}'
    if len != 0 and exact == False:
        final = final + str(len) + "+"
    if len == 0 and exact == False:
        final = final + '+'

    if position == 'end':
        final = final + '$'
        
    final = final + ')'
    
    columns = list(df)
    if colname in columns:
        extr = df[colname].str.extract(final, expand= False)
        df[colname] = pd.to_numeric(extr)
        infer_datatype_value(df, colname)
    else:
        for i in columns:
            col = i[0]
            if col == colname:
                extr = df[i].str.extract(final, expand= False)
                df[i] = pd.to_numeric(extr)
                infer_datatype_value(df, i)
                break

def boolean_db_contains(df, colname, string, newcolname= None):
    """
    Creates a column that expresses whether or not a substring is within
    each cell for a certain column.
    'df' is the dataframe; 'colname' is the column name to check; 'string' is
    the substring to search for; 'newcolname' is the name of the column that
    the boolean values should have
    """
    columns = list(df)
    full = False
    if colname in columns:
        ex = df[colname].str.contains(string)
        full = True
    else:
        columns = list(df)
        for i in columns:
            col = i[0]
            if col == colname:
                ex = df[i].str.contains(string)
                break

    if newcolname == None:
        newcolname = 'Contains ' + string
    if full:
        df.insert(df.columns.get_loc(colname) + 1, newcolname, [str(i) for i in list(ex)], True)
    else:
        df.insert(df.columns.get_loc(i) + 1, newcolname, [str(i) for i in list(ex)], True)
    
    infer_datatype_value(df, newcolname)

def remove_row_containing(df, colname, string):
    """
    Finds every row in column 'colname' that contains the str 'string'
    and removes it.
    'df' is the dataframe, 'colname' is the column name and 'string'
    is the str
    """
    columns = list(df)
    if colname not in columns:
        for i in columns:
            col = i[0]
            if col == colname:
                colname = i

    ex = df[colname]
    ex_list = list(ex)
    temp = []
    for i in range(len(ex_list)):
        if string in ex_list[i]:
            temp.append(df.iloc[i].name)

    remove_rows(df, temp)

    infer_datatype_values(df)

    # df[~df[colname].isin([string])]

def split_at_char(df, colname, string, newcolname):
    """
    Splits the column 'colname' into two at 'string'. ('string'
    not included)
    'df' is the Dataframe, 'colname' is the column to search for
    the str 'string', 'string' is where the column gets split, and
    'newcolname' is the name the new column will have
    """
    columns = list(df)
    if colname not in columns:
        for i in columns:
            col = i[0]
            if col == colname:
                colname = i

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
    columns = list(df)
    if colname in columns:
        temp = df[colname]
        conditional = temp.str.contains(str1)
        df[colname] = np.where(conditional, str2, temp.str.replace('', ''))
        infer_datatype_value(df, colname)
    else:
        for i in columns:
            col = i[0]
            if col == colname:
                temp = df[i]
                conditional = temp.str.contains(str1)
                df[i] = np.where(conditional, str2, temp.str.replace('', ''))
                infer_datatype_value(df, i)
                break

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

def change_header_row(filename, rownum):
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
    df.reset_index(drop= True)

def combine_cols(df, col1, col2):

    """
    Combines two columns, 'col2' gets merged with 'col1' while
    'col2' gets deleted
    'df' is a Dataframe, 'col1' is the name of the column that
    changes, and 'col2' is the name of the column that merges
    """
    columns = list(df)
    if col1 not in columns:
        for i in columns:
            col = i[0]
            if col == col1:
                col1 = i
    if col2 not in columns:
        for i in columns:
            col = i[0]
            if col == col2:
                col2 = i

    ex1 = df[col1]
    ex2 = df[col2]
    ex1_list = list(ex1)
    ex2_list = list(ex2)

    final = []
    if type(ex1_list[0]) == type(ex2_list[0]):
        for i in range(len(ex1_list)):
            temp = ex1_list[i] + ex2_list[i]
            final.append(temp)
    else:
        for i in range(len(ex1_list)):
            temp = str(ex1_list[i]) + ' ' + str(ex2_list[i])
            final.append(temp)
    
    df[col1] = final

    remove_cols(df, col2)

    infer_datatype_values(df)

def enumerate_regex(selection):
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

    columns = list(df)
    
    if col not in columns:
        for i in columns:
            colname = i[0]
            if colname == col:
                col = i

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
            elif re.search('^\d\d?[-/]\d\d?[-/]\d\d\d?\d?$', data) != None:
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

    # mapping[col].type = new_type

    rename_cols(df, {col: (col[0], new_type + " #LOCKED#")})

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

    columns = list(df)
    final = []
    for col in cols:
        if col not in columns:
            for i in columns:
                colname = i[0]
                if colname == col:
                    final.append(i)
                    break
        else:
            final.append(col)

    df.sort_values(by= final, ascending= ascend, na_position= Nan, inplace= True)

def apply_func_to_col(df, func, col):
    columns = list(df)
    if col not in columns:
        for i in columns:
            colname = i[0]
            if colname == col:
                col = i
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
    df[col] = df[col].str.replace('\d+', '')

def remove_letters(df, col):
    df[col] = df[col].str.replace('[a-zA-Z]+', '')

def remove_whitespace(df, col):
    df[col] = df[col].str.replace('\s+', '')

def keep_letters(df, col):
    df[col] = df[col].str.replace('[^a-zA-Z]+', '')

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
"""