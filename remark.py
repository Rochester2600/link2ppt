#!/usr/bin/python
# Title: Remark.py
# Description: Class to convert to remarkjs presentations


### TODO Change this
## planned on implementing: sourceUrl: 'markdown.md'

class Remark:
    def __init__(self, template=None):
        ## Create new remark instance
        self.slides = []

    def add_slide(self, slide):
        """ Receive a dict containing title, highlights(list), and url
        slide["title"], slide["url"], slide["higlights"] """
        content = []
        #content.append("class: center, middle") ##TODO change to dynamic
        content.append("## " + slide["title"])
        highlights = []
        for h in slide["highlights"]:
            content.append("- " + h)
        content.append(slide["url"])
        content.append("---")
        self.slides.append(content)

    def _test_slide(self):
        slide = {}
        slide["title"] = "Test title"
        slide["url"] = "Http://www.google.com"
        highlights = ["Highlight 1", "more", "Something else"]
        slide["highlights"] = highlights
        return slide

    def build(self):
        """ Returns just the MD of the slides"""
        md = ""
        for slide in self.slides:
            for line in slide:
                md += line + "\n\n"
        return md


if __name__ == '__main__':
    print("")
