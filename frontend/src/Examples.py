
mapping = {}

def create_dictionary():
    #creating a dictionary to map clicks to functions
    columns = list(df)
    rows = list(df.index)

    for col in columns:
        mapping[('Remove', col)] = 'dcf.remove_cols(df, ' + str(col) + ')'

    for row in rows:
        mapping[('Remove', row)] = 'dcf.remove_rows(df, ' + str(row) + ')'

def create_dictionary_each_cell():
    #this may be too time consuming and can be scrapped
    columns = list(df)
    rows = list(df.index)

    for col in columns:
        for row in rows:
            mapping[('Remove', col, row)] = 'dcf.remove_value(df, ' + str(col) + ', ' + str(row) + ')'

def update_mapping(new):
    #adds all the methods for new cols or rows but would end up being really long code
    columns = list(df)
    rows = list(df.index)
    col = True

    if new in columns or new in rows:
        mapping[('Remove', new)] = 'dcf.remove_cols(df, ' + str(new) + ')'
        if new in rows:
            col = False
    if col:
        for row in rows:
            mapping[('Remove', new, row)] = 'dcf.remove_value(df, ' + str(new) + ', ' + str(row) + ')'
    else:
        for col in columns:
            mapping[('Remove', col, new)] = 'dcf.remove_value(df, ' + str(col) + ', ' + str(new) + ')'

#to keep dictionaries as small as possible
#cleaning methods:

def cleaning_option1():
    #take out all outdated commands, and then add all new ones
    prev = colname
    dcf.rename_cols(df, {colname: new})
    for command in mapping:
        if prev in command:
            del command
    update_mapping(new)

def cleaning_option2():
    #recreate the mapping, most likely preferrable in cases where multiple cols/rows/cells are removed
    create_dictionary()
