"""
models.py

App Engine datastore models

"""


from google.appengine.ext import db


class ExampleModel(db.Model):
    """Example Model"""
    example_id = db.StringProperty(required=True)
    example_title = db.StringProperty(required=True)
    added_by = db.UserProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)

class Providers(db.Model):
	"""Provider Information DB"""
	pDomain = db.StringProperty()
	pType = db.StringProperty()
	pAgency = db.StringProperty()
	pSite = db.StringProperty()
	programName = db.StringProperty()
	pAddress = db.StringProperty()
	pAddress2 = db.StringProperty()
	pCity = db.StringProperty()
	pState = db.StringProperty()
	pZip = db.StringProperty()
	pPhone = db.StringProperty()
	pEmail = db.StringProperty()
	pNotes = db.TextProperty()
	Owner = db.UserProperty()
	
class ProviderNotes(db.Model):
	"""Provider Notes will be captured in this database"""
	provider_name = db.StringProperty()
	provider_notes = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	