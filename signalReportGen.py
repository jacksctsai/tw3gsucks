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

from datetime import tzinfo, timedelta, datetime

class ShowMap2Page(webapp.RequestHandler):
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
            
        signal.dateStr = (signal.date + timedelta(hours=+8)).strftime("%Y-%m-%d %H:%M:%S");

        template_values = {
            'signals': signals
        }
        if self.request.get('location') == '':
          template_values['location'] = "24.774922,121.044976"
        else:
          template_values['location'] = self.request.get('location')

        path = os.path.join(os.path.dirname(__file__), 'showMap2.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
  ('/showMap', ShowMap2Page)
], debug=True)


def main():
  run_wsgi_app(application)
