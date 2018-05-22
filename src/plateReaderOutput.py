
import pandas as pd
import utils
import sys
import os
import re
import math

LONG_COLUMN_LIST = ['row', 'column', 'sample']

def toDfValue(val):
    if val == "":
        return None
    if val == "#Sat":
        return math.inf
    else:
        return float(val)


def readMapTemplate(fname, format):

    #read template and convert to long format if necissary
    template = pd.read_csv(fname, sep = '\t')
    if format == "wide":
        template = template.melt(id_vars = ['row'], value_vars = [str(x) for x in list(range(1, 13))],
                      var_name = "column", value_name = 'sample')

    #check that template has required column names
    if LONG_COLUMN_LIST != template.columns.tolist():
        sys.stderr.write("Map template does not have valid format!\n")
        return None

    template['cell'] = template['row'] + template['column'].map(str)
    template = template.drop(['row', 'column'], axis = 1)

    return template


def getRawInput(fname):
    #open file
    if os.path.exists(fname):
        inF = open(fname, 'rb')
        dat = inF.read()
    else:
        sys.stderr.write("File does not exist!\n")
        return None

    #use manual fxns to decode ISO-8859 or utf-8 encoding
    try:
        lines = utils.bytesToLines(dat)
    except UnicodeDecodeError:
        sys.stderr.write("Unknown character encoding detected!\n")
        return None

    nBlocks = int(lines[0].split('=')[1].strip())
    if nBlocks != 1:
        raise NotImplementedError("More than 1 block detected")

    headers = lines[2].split('\t')
    values = lines[3].split('\t')
    assert(len(headers) == len(values))

    df = pd.DataFrame(columns = ['block', 'cell', 'value'])

    #itterate through headers and values elements
    for i in range(0, len(headers)):
        #check if current index is cell header
        if re.match('^[A-H][0-9]+$', headers[i]):
            df.loc[i] = [1, headers[i], toDfValue(values[i])]

    #df = df.melt(id_vars = row)
    df = df.reset_index(drop = True)

    return df




