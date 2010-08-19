#!/usr/bin/env python
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp \
    import template
from google.appengine.api import urlfetch
import json
from webob import Request
import cgi

#google_appengine/dev_appserver.py ./guestbook
#

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
                self.lng = float(json_ob['Placemark'][0]['Point']['coordinates'][0])
                self.lat = float(json_ob['Placemark'][0]['Point']['coordinates'][1])
                self.name = json_ob['name'].encode(encoding)
                self.result = 1
            else:
                self.result = 0
        else:
            self.result = 0
#asdasdasd
#sadas
class GoogleGeo(webapp.RequestHandler):
    def __calc_pos(self,p1,p2):
        if p1.result==1 and p2.result==1:
            if p2.lat == p1.lat and p2.lng == p1.lng:
                text = "同じ場所です"
            elif float(p2.lat-p1.lat)/float(p2.lng-p1.lng) <= 1:
                if p1.lng-p2.lng>0:
                    text = "%sが右、%sが左にあります。" % (p1.name,p2.name)
                else:
                    text = "%sが左、%sが右にあります。" % (p1.name,p2.name)
            else:
                if p2.lat<p1.lat:
                    text = "%sが上、%sが下にあります。" % (p1.name,p2.name)
                else:
                    text = "%sが下、%sが上にあります。" % (p1.name,p2.name)

        else:
            text = "Error"
        return text


    def post(self):
        encoding = 'utf-8'
        ad1 = cgi.escape(self.request.get('ad1'))
        ad2 = cgi.escape(self.request.get('ad2'))
        p1 = GoogleMapGeo(ad1.encode(encoding))
        p2 = GoogleMapGeo(ad2.encode(encoding))
        text = self.__calc_pos(p1,p2)
        self.response.out.write(
            template.render('geo.html',
                            {'message':text}))


    def get(self):
        p1 = GoogleMapGeo("鳥取")
        p2 = GoogleMapGeo("島根")
        text = self.__calc_pos(p1,p2)
        self.response.out.write(
            template.render('geo.html',
                            {'message':text}))

def main():
    app = webapp.WSGIApplication([
            (r'.*',GoogleGeo)],debug = True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__  == "__main__":
    main()


#google_appengine/dev_appserver.py ./RightorLeft/
