#!/usr/bin/python
# Title: Link2PPT
# Description: Automatic PPTX generator used by
# Rochester2600 group to build a list of links
# Each month.
# Usage: ./l2ppt links.csv
# CSV format:
# url, date, authors

import csv, argparse, subprocess
import logging, sys
try:
    import pptx
except:
    print("No pptx module!")
    sys.exit()
try:
    import pocket
except:
    print("No pocket support")
import urllib2
try:
    from BeautifulSoup import BeautifulSoup
except:
    print("Missing beautifulsoup module")
    sys.exit()

OUTPUT = ""

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
    #parser.add_argument('-o',
    #    dest='output,
    #    help='Command line import')
    parser.add_argument('-x',
        dest='ppt',
        help="Update an existing ppt")
    parser.add_argument('-p',
        dest='pocket',
        help="Update an existing ppt")

    args = parser.parse_args()
    OUTPUT = "2600report.pptx"
    #if args.ppt:
    #    ## -x update an existing pptp
    #    ppt = args.ppt
    #else:
    #    ppt = Presentation()
    ## [default] file
    if args.csv:
        ### if file, then for each line do parse csv
        parse_csv(args.csv)
    elif args.pocket:
        getpocket()
    else:
        print("Try -h for help")

    ## -c command line url, author (autodate)
    ### if command, parse line input, add date

    #prs = pptx.Presentation()
def add_slide(line):
    '''Needs a dict of title and url at least'''
    prs = pptx.Presentation(OUTPUT)
    title_slide_layout = prs.slide_layouts[1]
    #for line in csvobj:
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = line["title"]
    subtitle.text = line["url"]
    prs.save(OUTPUT)


def get_pocket():
    print("TODO")

def get_title(url):
    try:
        f = urllib2.urlopen(url)
        soup = BeautifulSoup(f)
        f.close()  #Trying to limit memory usage
    except:
        logging.error("URL: %s had an error" % url)
        return "Blank"
    logging.debug("Title found as: %s" % soup.title.string)
    if soup.title.string:
        return soup.title.string
    else:
        return "No title found"


def parse_csv(file):
    # is csv file?
    csvobj = []
    with open(file, 'rb') as csvfile:
        urllist = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in urllist:
            ## If url TODO
            record = {}
            record["url"] = row[0]
            try:
                record["author"] = row[1]
            except IndexError:
                record["author"] = None

            try:
                record["date"] = row[2]
            except IndexError:
                record["date"] = None
            sspath = screenshot(record["url"])

            if sspath:
                logging.debug("Screenshot complete")
                record["screenshot"] = sspath
                #row.append(sspath)
            else:
                logging.error("Screenshot failed")
                record["screenshot"] = None
            record["title"] = get_title(row[0])

            ## add to slide
            add_slide(record)

            csvobj.append(record)  # test
    return csvobj


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
            "Make sure you are running with an X session"
            % (out, err)
        )
        return None
    else:
        return outputfile


if __name__ == '__main__':
    # init main
    main()
