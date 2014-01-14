from flask import render_template
from flask.ext.appbuilder.baseapp import BaseApp
from flask.ext.appbuilder.models.datamodel import SQLAModel
from flask.ext.appbuilder.views import GeneralView, BaseView, IndexView, expose
from app import app, db

class FABView(IndexView):
    """
        A simple view that implements the index for the site
    """
    index_template = 'index.html'

class ContactsView(IndexView):
    route_base = "/contacts"
    index_template = 'contacts.html'
    @expose('/')
    def index(self):
        return render_template(self.index_template, baseapp = self.baseapp)


baseapp = BaseApp(app, db, indexview = FABView)
baseapp.add_view(ContactsView(), "Contacts", href='/contacts',icon='fa-phone')
