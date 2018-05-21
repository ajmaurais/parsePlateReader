
import argparse
import sys

PROG_VERSION = "1.0"

def main():
    parser = argparse.ArgumentParser(description= "Format plate reader text output to a layout which is actually useful.",
                                     epilog = "parsePlateReader was written by Aaron Maurais.  "
                                              "Email questions or bugs to aaron.maurais@bc.edu",
                                     prog = "parsePlateReader")

    parser.add_argument("map_file", help = "")
    parser.add_argument("data_file", nargs = '+', help = "data file to read")

    parser.add_argument("--version", action='version', version='%(prog)s ' + PROG_VERSION)

    args = parser.parse_args()



if __name__ == "__main__":
    main(sys.argv)



