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

from reportsignal import SignalReport

class MainPage(webapp.RequestHandler):
    def get(self):
        signal_query = SignalReport.all()
        signals = signal_query.fetch(signal_query.count())
        
        for signal in signals:
          if signal.speed >= 2000:
          	signal.Excellent = 1
          elif signal.speed >= 1000 and signal.speed < 2000:
            signal.Good = 1
          elif signal.speed >= 500 and signal.speed < 1000:
            signal.Poor = 1
          else:
            signal.Bad = 1

        template_values = {
            'signals': signals
        }

        path = os.path.join(os.path.dirname(__file__), 'signalReportTemplate.kml')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
  ('/signalReport.kml', MainPage)
], debug=True)


def main():
  run_wsgi_app(application)
