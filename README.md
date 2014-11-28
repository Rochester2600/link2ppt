link2ppt
========

Automatically generates a Powerpoint presentation of links and content. Designed for a monthly 2600 meeting. 

## Features:##

* Collects links and highlights from an instapaper account and puts them into a PPTX
* Takes in CSV of url, author, date and pushes into a PPTX
* Downloads a PDF copy of the site
* Supports using PPTX templates

##TODO:##

* Collect from other sources besides csv and instapaper

## Requirements ##

* Python-pptx
 pip install python-pptx
* Requests
 pip install requests
 
## Optional ##

* wkhtmltopdf (for pdf generation)
 apt-get install wkhtmltopdf
* BeautifulSoup (for csv import)