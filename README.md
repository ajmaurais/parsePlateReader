# parsePlateReader
Format plate reader text output to a layout which is actually useful

## Usage
```
usage: parsePlateReader [-h] [--version] [-m MAPPATH] [--blankMap]
                        [-f {wide,long}] [-w] [-o OFNAME] [-n] [-c]
                        data_file [data_file ...]

Format plate reader text output to a layout which is actually useful.

positional arguments:
  data_file             data file to read

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -m MAPPATH, --mapPath MAPPATH
                        Path to map file for sample names. Use --blankMap to
                        print blank map.
  --blankMap            Print map file template and exit.
  -f {wide,long}, --mapFormat {wide,long}
                        Specify how map is formated.
  -w, --wideOutput      Also output wide formated file without sample names.
  -o OFNAME, --ofname OFNAME
                        Specify output file name.
  -n, --na              Specify whether to include rows where the value col is
                        NA in output file. By default NAs are not included.
  -c, --combineOutput   Combine all output files into one. By default one
                        output file is generated for each input file.
 ```
