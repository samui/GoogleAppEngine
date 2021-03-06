#!/usr/bin/python
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp \
    import template
from google.appengine.api import urlfetch
import json
from webob import Request
import cgi

class GoogleMapGeo():
    RequestUrl = "http://maps.google.com/maps/geo"
    key = "ABQIAAAAkAS0BwHhvwaYvSlKqAf_4xT2yXp_ZAY8_ufC3CFXhHIE1NvwkxQ_YvfaI_8VHj8iIk88AJwclNWJdg"
    def __init__(self,address):
        encoding = 'utf-8'
        url = "%s?&q=%s&key=%s" % (self.RequestUrl,address,self.key )
        self.place = address
        doc = urlfetch.fetch(url)
        if doc.status_code  == 200:
            json_ob = json.loads(doc.content)
            if json_ob['Status']['code'] != 602:
                print json_ob
                self.lng = float(json_ob['Placemark'][0]['Point']['coordinates'][0])
                self.lat = float(json_ob['Placemark'][0]['Point']['coordinates'][1])
                self.name = json_ob['name'].encode(encoding)
                self.result = 1
                self.wantPlace = ""
                i = 0
                while i<len(json_ob['Placemark']):
                    #self.wantPlace+=(json_ob['Placemark'][i]['address']).replace("[\w]","")
                    placedetail = json_ob['Placemark'][i]['AddressDetails']['Country']
                    self.wantPlace+=json_ob['Placemark'][i]['address']
                    self.wantPlace+= "   "

                    i+= 1

            else:
                self.result = 0
        else:
            self.result = 0




if __name__  == "__main__":
    p1 = GoogleMapGeo("Tokyou")
