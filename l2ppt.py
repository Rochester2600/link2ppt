#!/usr/bin/python
# Title: Link2PPT
# Description: Automatic PPTX generator used by
# Rochester2600 group to build a list of links
# Each month.
# Usage: ./l2ppt links.csv
# CSV format:
# url, date, authors

import csv, argparse, subprocess
import logging


class ClassName(object):
    """2600 Powerpoint CLass"""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg


def main():
    # Handle arguments
    parser = argparse.ArgumentParser(
        description='Convert links to ppt')
    parser.add_argument("-f",
        dest='csv',
        help='csv file')
    #parser.add_argument('-c',
    #    dest='line,
    #    help='Command line import')
    parser.add_argument('-x',
        dest='ppt',
        help="Update an existing ppt")

    args = parser.parse_args()

    #if args.ppt:
    #    ## -x update an existing pptp
    #    ppt = args.ppt
    #else:
    #    ppt = Presentation()
    ## [default] file
    if args.csv:
        ### if file, then for each line do parse csv
        parse_csv(args.csv)

    ## -c command line url, author (autodate)
    ### if command, parse line input, add date

    print("hello")


def parse_csv(file):
    # is csv file?
    with open(file, 'rb') as csvfile:
        urllist = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in urllist:
            ## If url TODO
            ss = screenshot(row[0])

            print(row)  # test


def screenshot(url):
    # screenshot url
    ## http://wkhtmltopdf.org/
    outputfile = "%s.pdf" % url  #TODO strip!!
    commands = ["wkhtmltopdf", url, outputfile]
    exe = subprocess.Popen(commands, stdout=subprocess.PIPE)
    out, err = exe.communicate()
    if exe.returncode != 0:
        logging.debug(
            "Error executing shell command: \n"
            "Output\n%s\n"
            "Errors:\n%s\n"
            % (out, err)
        )
    else:
        return(outputfile)

    print("Incomplete")


# add slide(url, screenshot)


if __name__ == '__main__':
    # init main
    main()
