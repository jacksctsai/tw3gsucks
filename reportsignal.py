import cgi
import datetime
import urllib
import wsgiref.handlers
import os
from google.appengine.ext.webapp import template

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class SignalReport(db.Model):
  """Models an individual signal report entry, geolocation, connection info, ip address, and date."""
  location = db.GeoPtProperty()
  speed = db.IntegerProperty()
  tech = db.StringProperty()
  provider = db.StringProperty()
  ip = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, []))
		
	def post(self):
		#self.response.out.write('location:'+self.request.get('location'))
		#self.response.out.write('provider_tech:'+self.request.get('provider_tech'))
		location = self.request.get('location').split(', ')
		provider_tech = self.request.get('provider_tech').split(' ')
		speed = self.request.get('speed')
		signalReport = SignalReport()
		if speed.isdigit():
			signalReport.speed = int(speed)
		signalReport.location = db.GeoPt(lat = location[0], lon=location[1])
		signalReport.tech = provider_tech[1]
		signalReport.provider = provider_tech[0]
		signalReport.ip = self.request.remote_addr
	
		signalReport.put()
		self.redirect('/reportSaved?location='+self.request.get('location')+'&speed='+self.request.get('speed'))

class ShowMapPage(webapp.RequestHandler):
    def get(self):

        path = os.path.join(os.path.dirname(__file__), 'showMap.html')
        templateValues = {'location': ''};
        if self.request.get('location') == '':
          templateValues['location'] = "24.774922,121.044976"
        else:
          templateValues['location'] = self.request.get('location')
        self.response.out.write(template.render(path, templateValues))

class ReportSaved(webapp.RequestHandler):
    def get(self):

        path = os.path.join(os.path.dirname(__file__), 'reportSaved.html')
    	templateValues = {'location': self.request.get('location'), 'speed': self.request.get('speed'), 'speedInMB': int(self.request.get('speed'))/1024};
        self.response.out.write(template.render(path, templateValues))

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/showMap', ShowMapPage),
  ('/reportSaved', ReportSaved)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()