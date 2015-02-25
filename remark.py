#!/usr/bin/python
# Title: Remark.py
# Description: Class to convert to remarkjs presentations


### TODO Change this
## planned on implementing: sourceUrl: 'markdown.md'

class Remark:
    def __init__(self, template=None):
        ## Create new remark instance
        self.slides = []
        self.md = []

    def build_slides(self):
        """ Receive a dict containing title, highlights(list), and url
        slide["title"], slide["url"], slide["higlights"] """
        md = ""
        for slide in reversed(self.slides):
            content = []
            #content.append("class: center, middle") ##TODO change to dynamic
            content.append("## " + slide["title"])
            highlights = []
            for h in slide["highlights"]:
                content.append("- " + h)
            content.append("[" + slide["url"] + "](" + slide["url"] + ")")
            content.append(".footnote[%s]" % slide["category"])
            content.append("---")

            for line in content:
              md += line + "\n\n"
        return md

    def add_slide(self, slide):
        self.slides.append(slide)

    def _test_slide(self):
        slide = {}
        slide["title"] = "Test title"
        slide["url"] = "http://www.google.com"
        highlights = [
            "Highlight item #1",
            "this is a long highlight about something or other. It's not very interesting",
            "Something else"
        ]
        slide["highlights"] = highlights
        return slide

    def add_agenda(self):
        slide = {}
        slide["title"] = "Agenda"
        titles = []
        for s in self.slides:
            titles.append(s["title"])
        slide["highlights"] = titles
        slide["url"] = ""
        slide["category"] = "Random"
        self.add_slide(slide)

    def build(self):
        """ Returns just the MD of the slides"""
        self.add_agenda()
        md = self.build_slides()
        return md

if __name__ == '__main__':
    print("")
