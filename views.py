"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""


from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.ext import db


from flask import render_template, flash, url_for, redirect, request, make_response
from wtforms.ext.appengine.db import model_form
from flaskext import wtf
from flaskext.wtf import validators, Form


from models import ExampleModel, Providers, ProviderNotes
from decorators import login_required, admin_required
from forms import ExampleForm, ProviderForm

@login_required
def home():
	return redirect(url_for('list_provs'))

@login_required	
def list_provs():
#	owner = users.get_current_user()
#	print owner
	providers = []
	provs = Providers.all().order('pAgency')
#	provs = db.Query(Providers).filter('Owner =', owner).order('pAgency')
	for prov in provs:
		if prov.pAgency in providers:
			pass
		else:
			providers.append(prov.pAgency)
	return render_template('providers.html', providers=providers) #, owner=owner
	
@login_required	
def list_addresses(agency):
	address_program_pairs = []
	addresses = db.Query(Providers).filter('pAgency =', agency).order('pAddress')
	for addr in addresses:
		address_program_pairs.append((addr.pAddress, {'name' : addr.programName , 'type' : addr.pType , 'phone' : addr.pPhone}))
	grouped_addrs = {}
	for elt in address_program_pairs: 
		if elt[0] in grouped_addrs:
			grouped_addrs[elt[0]].append(elt[1])
		else:
			grouped_addrs[elt[0]] = [elt[1]]
	return grouped_addrs

@login_required
def list_notes(agency):
	notes_query = db.Query(ProviderNotes).filter('provider_name =', agency)
	notes = []
	for note in notes_query:
		notes.append(note.provider_notes)
	return notes

@login_required
def add_notes(agency):
 	MyForm = model_form(ProviderNotes, Form)
 	entity = db.Query(ProviderNotes).filter('provider_name =', agency).get()
 	if entity != None:
		form = MyForm(request.form, obj=entity)
		if form.validate_on_submit():
			form.populate_obj(entity)
			entity.put()
			flash(u'Example successfully saved.', 'success')
			return redirect(url_for('list_provs'))
	else:
		form = MyForm(request.form)
		if form.validate_on_submit():
			notes = ProviderNotes(
				provider_name=agency,
				provider_notes=form.provider_notes.data)
			notes.put()
			flash(u'Example successfully saved.', 'success')
			return redirect(url_for('list_provs'))
	return render_template('provider_notes.html', form=form, programs=list_addresses(agency), pname=agency, notes=list_notes(agency))


# @login_required
# def add_notes(agency):
# 	form = ProviderForm()
# 	if form.validate_on_submit():
#  		notes = ProviderNotes(
#  			provider_name = agency,
#  			provider_notes = form.providerNote.data)
#  		try:
#  			notes.put()
#  			flash(u'Example successfully saved.', 'success')
#  			return redirect(url_for('list_provs'))
#  		except:
# 	 		return redirect(url_for('list_provs'))
# 	return render_template('provider_notes.html', form=form, programs=list_addresses(agency), pname=agency, notes=list_notes(agency))

def warmup():
	"""App Engine warmup handler
	See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

	"""
	return ''

