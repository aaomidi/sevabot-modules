#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get the definition of a word
"""
import os
import sys
import httplib
import random
import urllib
from pyquery import PyQuery as pq


def define(args):
    word = " ".join(args)

    if word == "Amir":
        word = "amir"


    wordParam = urllib.quote_plus(word)

    conn = httplib.HTTPConnection("www.urbandictionary.com")
    url = "/define.php?term=" + wordParam
    conn.request("GET", url, None, {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/191.238.50.22 Safari/537.36", "Host" : "www.urbandictionary.com"
    })

    print "Definition of: " + word

    response = conn.getresponse()

    doc = pq(response.read())

    meaning = doc.find(".meaning")

    if len(meaning) > 0:
        strippedHtml = meaning.html().replace("<br/>", "\n")
        print pq(strippedHtml).text().encode("utf-8")

    else:
        conn = httplib.HTTPConnection("m.dictionary.com")
        url = "/definition/" + wordParam
        conn.request("GET", url, None, {
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/191.238.50.22 Safari/537.36", "Host" : "www.urbandictionary.com"
        })
        response = conn.getresponse()

        doc = pq(response.read())

        resultItem = doc.find("#embed_dresultitem_r3")

        if len(resultItem) > 0:
            print "Definition of: " + word

            for result in resultItem.children():
                text = ""

                for child in pq(result).children():
                    text += pq(child).text()

                print text.encode("utf-8")
        else:        
           print "No definition for " + word + ". Try to change the casing."

define(sys.argv[1:])