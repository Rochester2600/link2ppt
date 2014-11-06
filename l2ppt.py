#!/usr/bin/python
# Title: Link2PPT
# Description: Automatic PPTX generator used by
# Rochester2600 group to build a list of links
# Each month.
# Usage: ./l2ppt links.csv
# CSV format:
# url, date, authors

import csv


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
            print(row)  # test


def screenshot(url):
    # screenshot url
    ##TODO screenshot library
    print("Incomplete")


# add slide(url, screenshot)


if __name__ == '__main__':
    # init main
    main()
