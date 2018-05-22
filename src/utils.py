
import re

UTF8_STR = 'utf-8'
ISO8859_STR = 'ISO-8859-1'

#returns true of bytes is encoded in utf-8
def isUTF8(bytes):
    try:
        s = bytes.decode(UTF8_STR)
    except UnicodeDecodeError:
        return False
    else:
        return True

#returns true of bytes is encoded in ISO-8859
def isISO8859(bytes):
    try:
        s = bytes.decode(ISO8859_STR)
    except UnicodeDecodeError:
        return False
    else:
        return True

#converts bytes to string
def bytesToStr(bytes):
    if isUTF8(bytes):
        s = bytes.decode(UTF8_STR)
    elif isISO8859(bytes):
        s = bytes.decode(ISO8859_STR)
    else:
        raise UnicodeDecodeError
    return s

#converts bytes to list of strings by new line chars
def bytesToLines(bytes):
    s = bytesToStr(bytes)
    lines = s.rsplit('\r\n')
    return lines
