
import pandas as pd
import sys
import os
import re
import math

from .utils import bytesToLines
# 
LONG_COLUMN_LIST = ['row', 'column', 'sample']

def _toDfValue(val):
    if val == "":
        return None
    if val == "#Sat":
        return math.inf
    else:
        return float(val)


def _parseTime(val):
    s = val.split(':')
    ret = 0
    for i in range(3):
        try:
            ret += (int(s[-(i+1)]) * pow(60, i))
        except IndexError:
            break

    return ret

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
        lines = bytesToLines(dat)
    except UnicodeDecodeError:
        sys.stderr.write("Unknown character encoding detected!\n")
        return None

    nBlocks = int(lines[0].split('=')[1].strip())
    if nBlocks != 1:
        raise NotImplementedError("More than 1 block detected")

    #get time format
    metadata = lines[1].split('\t')
    try:
        timeFormat = metadata[metadata.index('TimeFormat') + 1]
    except ValueError:
        sys.stderr.write('Failed to find TimeFormat!')
        return None
    sys.stdout.write("found '{}' time format.\n".format(timeFormat))

    columns = lines[2].split('\t')

    #itterate through headers get indecies of values
    colDict = dict()
    for i in range(0, len(columns)):
        #check if current index is cell header
        match = re.search('^([A-H][1-9][0-2]?)$', columns[i])
        if match:
            colDict[match.group(1)] = i

    colnames = ['block', 'cell', 'value']
    _index = 0
    if timeFormat == 'Endpoint':
        df = pd.DataFrame(columns=colnames)

        values = lines[3].split('\t')
        if len(columns) != len(values):
            raise RuntimeError('Invalid row length!')
        for k, v in colDict.items():
            df.loc[_index] = [1, k, _toDfValue(values[v])]
            _index += 1

    elif timeFormat == 'Kinetic':
        colnames.append('time')
        _dat_temp = {k:list() for k in colnames}

        #get time col index
        timeIndex = columns.index('Time(hh:mm:ss)')

        for i in range(3, len(lines) - 1):
            #split row by \t
            values = lines[i].split('\t')

            #check that row contains data
            if len(values) == 1 and values[0] == '':
                continue
            if values[0] == '~End':
                break
            if len(columns) != len(values):
                sys.stdout.write('\nInvalid row length!')
                return None

            #itterate through columns
            timeTemp = _parseTime(values[timeIndex])
            for k, v in colDict.items():
                _dat_temp['block'].append(1)
                _dat_temp['cell'].append(k)
                _dat_temp['value'].append(_toDfValue(values[v]))
                _dat_temp['time'].append(timeTemp)

        df = pd.DataFrame(_dat_temp)

    else:
        sys.stderr.write('\nUnknown TimeFormat: '.format(timeFormat))
        return None

    df = df.reset_index(drop = True)

    return df

def getWide(df):
    #check that colnames are correct
    assert(df.columns.tolist() == ['block', 'cell', 'value'])

    #split cell col
    df['row'] = df['cell'].str[0:1]
    df['col'] = df['cell'].str[1:]
    df = df[['row', 'col', 'value']]

    #convert from long to wide
    df = df.pivot(index='row', columns='col', values='value')

    #reorder columns
    df = df[[str(x) for x in list(range(1,13))]]

    return df

