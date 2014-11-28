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
    import instalink
except:
    print("No Instapaper support")
import urllib2
try:
    from BeautifulSoup import BeautifulSoup
except:
    print("Missing beautifulsoup module")
    sys.exit()

#from guppy import hpy
#h = hpy()
#print h.heap()

OUTPUT = ""
CREDS = "./creds"


def main():
    global OUTPUT
    # Handle arguments
    parser = argparse.ArgumentParser(
        description='Convert links to ppt')
    parser.add_argument("-c",
                        dest='csv',
                        help='csv file')
    parser.add_argument('-i',
        dest='icreds',
        help='File with creds for instapaper')
    #parser.add_argument('-o',
    #    dest='output,
    #    help='Command line import')
    parser.add_argument('-x',
                        dest='ppt',
                        help="Update an existing ppt")
    parser.add_argument('-o',
                        dest='output',
                        help="Name of output PPTX file")

    args = parser.parse_args()
    OUTPUT = args.output
    CREDS = args.icreds
    #if args.ppt:
    #    ## -x update an existing pptp
    #    ppt = args.ppt
    #else:
    #    ppt = Presentation()
    ## [default] file
    if args.csv:
        ### if file, then for each line do parse csv
        parse_csv(args.csv)
    elif args.icreds:
        get_instapaper(args.icreds)
    else:
        print("Try -h for help")


def add_slide(line):
    global OUTPUT
    '''Needs a dict of title and url at least
    url'''
    prs = pptx.Presentation(OUTPUT)
    title_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(title_slide_layout)
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        text_frame = shape.text_frame
    text_frame.clear()
    title = slide.shapes.title
    content = slide.placeholders[1]
    bullets = "\n".join(line["highlights"])
    bullets += "\n" + line["url"]
    content.text = bullets
    title.text = line["title"]
    prs.save(OUTPUT)


def get_instapaper(creds):
    f = open(creds).read().splitlines()
    ilink = instalink.Instalink(f)
    ilink.login()
    il = ilink.getlinks()
    links = ilink.handlelinks(il)
    for s in links:
        add_slide(s)

def get_title(url):
    try:
        # 3s timeout
        f = urllib2.urlopen(url, tmeout=3000)
        soup = BeautifulSoup(f)
        f.close()

        if soup.title.string:
            logging.debug("Title found as: %s" % soup.title.string)
            return soup.title.string
        else:
            return "No title found"
    except:
        logging.error("URL: %s had an error" % url)
        return "Blank"


def parse_csv(file):
    # is csv file?
    #csvobj = []
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
            #sspath = screenshot(record["url"]) ## Disable mem issue
            sspath = None

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


def screenshot(url):
    # screenshot url
    ## http://wkhtmltopdf.org/
    outputfile = "%s.pdf" % url  # TODO strip!!
    commands = ["wkhtmltopdf", url, outputfile]
    try:
        if subprocess.call(commands) < 1:
            logging.debug(
                "Error executing shell command: \n"
                "Make sure you are running with an X session"
            )
            return None
        else:
            return outputfile
    except:
        logging.debug("Exception caught for wkhtmltopdf")
        return None


if __name__ == '__main__':
    # init main
    main()
