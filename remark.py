#!/usr/bin/python
# Title: Remark.py
# Description: Class to convert to remarkjs presentations


### TODO Change this
RHEADER = """
<!DOCTYPE html>
<html>
  <head>
    <title>Rochester 2600</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <style type="text/css">
      @import url(https://fonts.googleapis.com/css?family=Yanone+Kaffeesatz);
      @import url(https://fonts.googleapis.com/css?family=Droid+Serif:400,700,400italic);
      @import url(https://fonts.googleapis.com/css?family=Ubuntu+Mono:400,700,400italic);

      body { font-family: 'Droid Serif'; }
      h1, h2, h3 {
        font-family: 'Yanone Kaffeesatz';
        font-weight: normal;
      }
      .remark-code, .remark-inline-code { font-family: 'Ubuntu Mono'; }
    </style>
  </head>
  <body>
    <textarea id="source">
"""
RFOOTER = """
    </textarea>
    <script src="https://gnab.github.io/remark/downloads/remark-latest.min.js">
    </script>
    <script>
      var slideshow = remark.create();
    </script>
  </body>
</html>"""


class Remark:
    def __init__(self, template=None):
        ## Create new remark instance
        self.header = RHEADER
        self.footer = RFOOTER
        self.title = "2600 links"
        self.slides = []

    def add_slide(self, slide):
        """ Receive a dict containing title, highlights(list), and url
        slide["title"], slide["url"], slide["higlights"] """
        content = []
        content.append("class: center, middle") ##TODO change to dynamic
        content.append("## " + slide["title"])
        highlights = []
        for h in slide["highlights"]:
            content.append("- " + h)
        content.append(slide["url"])
        self.slides.append(content)

    def _test_slide(self):
        slide = {}
        slide["title"] = "Test title"
        slide["url"] = "Http://www.google.com"
        highlights = ["Highlight 1", "more", "Something else"]
        slide["highlights"] = highlights
        return slide

    def build(self):
        html = RHEADER
        for slide in self.slides:
            for line in slide:
                html += line + "\n\n"
        html += RFOOTER
        return html


if __name__ == '__main__':
    print("")
