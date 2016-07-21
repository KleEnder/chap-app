from google.appengine.ext import ndb

class Message(ndb.Model):
    text_entered = ndb.TextProperty()
    entry_date = ndb.DateTimeProperty(auto_now_add = True)