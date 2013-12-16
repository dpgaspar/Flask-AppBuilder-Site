from flask import render_template
from flask.ext.appbuilder.baseapp import BaseApp
from flask.ext.appbuilder.models.datamodel import SQLAModel
from flask.ext.appbuilder.views import GeneralView, BaseView, expose
from app import app, db

class FABView(BaseView):
    """
        A simple view that implements the index for the site
    """

    route_base = ''
    default_view = 'index'
    index_template = 'index.html'

    @expose('/')
    def index(self):
        return render_template(self.index_template, baseapp = self.baseapp)

class ContactsView(BaseView):
    route_base = "/contacts"
    index_template = 'contacts.html'
    @expose('/')
    def index(self):
        return render_template(self.index_template, baseapp = self.baseapp)


baseapp = BaseApp(app, db, indexview = FABView)
baseapp.add_view(ContactsView(), "Contacts", href='/contacts',icon='earphone',category='Info')
