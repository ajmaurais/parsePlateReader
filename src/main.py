
import argparse
import sys
import os
import pandas as pd
import csv

import modules as src
 
PROG_VERSION = "1.0"
PROG_SRC_DIR = os.path.dirname(os.path.realpath(__file__))
PROG_DIR = PROG_SRC_DIR[0:PROG_SRC_DIR.rfind('/')]
PROG_SHARE_DIR = PROG_DIR + "/share"
PROG_MAP_TEMPLATE = PROG_SHARE_DIR + "/mapTemplate.tsv"
DEFAULT_OFNAME = "namedValues.tsv"
WIDE_OFNAME = "wide.tsv"

def main(argv):

    #set up parser
    parser = argparse.ArgumentParser(description= "Format plate reader text output to a layout which is actually useful.",
                                     epilog = "parsePlateReader was written by Aaron Maurais.  "
                                              "Email questions or bugs to aaron.maurais@bc.edu",
                                     prog = "parsePlateReader")

    parser.add_argument("--version", action='version', version='%(prog)s ' + PROG_VERSION)

    parser.add_argument("data_file", nargs='+', help="data file to read")

    parser.add_argument("-m", "--mapPath", default = None, type = str,
                        help = "Path to map file for sample names. Use --blankMap to print blank map.")

    parser.add_argument('--blankMap', action='store_const', const=True, default=False,
                        help="Print map file template and exit.")

    parser.add_argument('-f', '--mapFormat', choices = ['wide', 'long'], default = 'wide',
                       help = "Specify how map is formated.")

    parser.add_argument("-w", "--wideOutput", action = 'store_const', default = False, const = True,
                        help = "Also output wide formated file without sample names.")

    parser.add_argument("-o", "--ofname", default = DEFAULT_OFNAME, help = "Specify output file name.")

    parser.add_argument('-n', '--na', action = 'store_const', default = False, const = True,
                        help = "Specify whether to include rows where the value col is NA in output file. "
                               "By default NAs are not included.")

    parser.add_argument('-c', '--combineOutput', action = 'store_const', const = True, default = False,
                        help = "Combine all output files into one. "
                               "By default one output file is generated for each input file.")

    #if user specified --blankMap option, print map template and exit
    if any([x == '--blankMap' for x in argv]):
        wd = os.getcwd()
        template = pd.read_csv(PROG_MAP_TEMPLATE, sep='\t')
        template.to_csv(path_or_buf = wd + "/mapTemplate.tsv", sep='\t',
                        quoting = csv.QUOTE_NONE, index = False, header = True,)
        exit()

    args = parser.parse_args()

    if not args.mapPath is None:
        sys.stdout.write('Reading mapTemplate...')
        template = src.readMapTemplate(os.path.abspath(args.mapPath), args.mapFormat)
        if template is None:
            exit()
        sys.stdout.write(' Done!\n')

    sys.stdout.write('Parsing data files...\n')
    all_data = pd.DataFrame(columns = ['file', 'block', 'cell', 'sample', 'value'])
    for file in args.data_file:
        sys.stdout.write('\tworking on {}... '.format(file))

        _file = os.path.abspath(file)
        df = src.getRawInput(_file)
        if df is None:
            exit()

        if args.wideOutput:
            wideOutput = src.getWide(df)
            wideOfname = src.getDuplicateOfname(os.path.abspath(WIDE_OFNAME),
                                                  os.path.splitext(os.path.basename(_file))[0])
            wideOutput.to_csv(path_or_buf = wideOfname, sep = '\t',
                              na_rep = "NA", quoting = csv.QUOTE_NONE, index = True)

        if args.mapPath is None:
            df_merged = df
        else:
            #join two data frames by cell and write out
            df_merged = df.merge(template, how = 'left', on = 'cell')

        #remove rows with na val col if specified
        if not args.na:
            navals = ~ df_merged['value'].isna()
            df_merged = df_merged[navals]

        if args.combineOutput:
            df_merged['file'] = os.path.basename(_file)
            all_data = all_data.append(df_merged, sort = False)[all_data.columns.tolist()]
        else :
            ofname = os.path.abspath(args.ofname)
            if len(args.data_file) > 1:
                ofname = getDuplicateOfname(ofname, os.path.splitext(os.path.basename(_file))[0])

            df_merged.to_csv(path_or_buf = ofname, sep = '\t',
                             na_rep = "NA", quoting = csv.QUOTE_NONE, index = False)

    if args.combineOutput:
        all_data.to_csv(path_or_buf = os.path.abspath(args.ofname), sep='\t',
                         na_rep="NA", quoting=csv.QUOTE_NONE, index = False)

    sys.stdout.write('Done!\n')

if __name__ == "__main__":
    main(sys.argv)



