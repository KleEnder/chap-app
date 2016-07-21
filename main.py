#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Message
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        list_of_m = Message.query().fetch()
        params = {"list_of_m": list_of_m}

        user = users.get_current_user()

        params["user"] = user

        if user:
            prijavljen = True
            logout_url = users.create_logout_url('/')

            params["prijavljen"] = prijavljen
            params["logout_url"] = logout_url
        else:
            prijavljen = False
            login_url = users.create_login_url('/')

            params["prijavljen"] = prijavljen
            params["login_url"] = login_url

        return self.render_template("main.html", params=params)


class MessageHandler(BaseHandler):
    def get(self):
        list_of_m = Message.query().fetch()
        params = {"list_of_m": list_of_m}

        user = users.get_current_user()

        params["user"] = user

        if user:
            prijavljen = True
            logout_url = users.create_logout_url('/')

            params["prijavljen"] = prijavljen
            params["logout_url"] = logout_url
        else:
            prijavljen = False
            login_url = users.create_login_url('/')

            params["prijavljen"] = prijavljen
            params["login_url"] = login_url


        return self.render_template("main.html", params=params)

    def post(self):
        input_message = self.request.get("input_message")

        message = Message(text_entered=input_message)
        message.put()

        #return self.write("You've entered: " + input_message)

        return self.redirect_to("main")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main"),
    webapp2.Route('/message', MessageHandler),
    #webapp2.Route('/all_messages', MessageHandler, name="all_messages"),
], debug=True)

