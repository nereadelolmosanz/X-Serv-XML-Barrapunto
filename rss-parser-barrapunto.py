#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Nerea Del Olmo Sanz - GITT
Titulares de barrapunto en página HTML (con link).
"""

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.sax import SAXParseException
import sys
import urllib


class myContentHandler (ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                # To avoid Unicode trouble
                self.newsTitle = (self.theContent + ".").encode('utf-8')
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                htmlNews = "      <li>\n"
                htmlNews += "        <a href='" + self.theContent + "' "
                htmlNews += 'target="_blank">'
                barrapuntoHTML.write(htmlNews)
                htmlNews = self.newsTitle + "</a>\n      </li>\n"
                barrapuntoHTML.write(htmlNews)
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


# --- Main prog
if len(sys.argv) < 2:
    print "Usage: python xml-parser-barrapunto.py <document>"
    print
    print " <URL RSS FILE>: url of the RSS document to parse"
    sys.exit(1)

# Load parser and driver
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!
try:
    #http://www.barrapunto.com/index.rss
    #Si no existe salta la excepcion y no se ejecuta nada mas
    #file descriptor
    rss = urllib.urlopen(sys.argv[1])

    barrapuntoHTML = open("barrapuntoRSS.html", "w")
    htmlStart = "<html>\n"
    htmlStart += "  <head>\n"
    htmlStart += "    <title>Barrapunto</title>\n"
    htmlStart += "    <meta charset='UTF-8'>\n"
    htmlStart += "  </head>\n\n"
    htmlStart += "  <body>\n"
    htmlStart += "    <div align=center>\n"
    htmlStart += "      <h1>Titulares Barrapunto</h1>\n"
    htmlStart += "    </div>\n"
    htmlStart += '    <HR align="center" size="2" width="450" color="black" noshade>\n'
    htmlStart += "    <ul type=square>\n"
    barrapuntoHTML.write(htmlStart)

    theParser.parse(rss)
    rss.close()

    htmlEnd = "    </ul>\n  </body>\n</html>"
    barrapuntoHTML.write(htmlEnd)
    barrapuntoHTML.close()

    print "Parse complete"
    sys.exit(0)

except SAXParseException:
    print "  Error: <" + sys.argv[1] + ">  does not exist"
    sys.exit(1)
