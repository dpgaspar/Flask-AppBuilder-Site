from flask import render_template, redirect
from flask.ext.appbuilder.models.datamodel import SQLAModel
from flask.ext.appbuilder.views import MasterDetailView, GeneralView, IndexView
from flask.ext.appbuilder.baseviews import expose
from flask.ext.appbuilder.charts.views import ChartView, TimeChartView
from flask.ext.babelpkg import lazy_gettext as _

from app import db, appbuilder
from models import Group, Gender, Contact


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()


class FABView(IndexView):
    """
        A simple view that implements the index for the site
    """
    index_template = 'index.html'


class ContactUsView(IndexView):
    route_base = "/contacts"
    index_template = 'contactus.html'

    @expose('/')
    def index(self):
        return render_template(self.index_template, baseapp=self.baseapp)


class ContactGeneralView(GeneralView):
    datamodel = SQLAModel(Contact, db.session)

    label_columns = {'group': 'Contacts Group'}
    list_columns = ['name', 'personal_celphone', 'birthday', 'group']

    base_order = ('name', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]


class ContactChartView(ChartView):
    chart_title = 'Grouped contacts'
    label_columns = ContactGeneralView.label_columns
    group_by_columns = ['group', 'gender']
    datamodel = SQLAModel(Contact, db.session)


class ContactTimeChartView(TimeChartView):
    chart_title = 'Grouped Birth contacts'
    chart_type = 'AreaChart'
    label_columns = ContactGeneralView.label_columns
    group_by_columns = ['birthday']
    datamodel = SQLAModel(Contact, db.session)


class GroupGeneralView(GeneralView):
    datamodel = SQLAModel(Group, db.session)
    related_views = [ContactGeneralView]
    #show_template = 'appbuilder/general/model/show_cascade.html'


class ConfigView(IndexView):
    route_base = "/config"

    @expose('/themes/<string:theme>')
    def index(self, theme=''):
        if theme == "default":
            self.baseapp.app_theme = ''
        else:
            self.baseapp.app_theme = "%s.css" % (theme)
        return redirect(self._get_redirect())

    @expose('/navreverse/')
    def navreverse(self):
        self.baseapp.menu.reverse = not self.baseapp.menu.reverse
        return redirect(self._get_redirect())


class GroupMasterView(MasterDetailView):
    datamodel = SQLAModel(Group, db.session)
    related_views = [ContactGeneralView]



fill_gender()
appbuilder.set_index_view(FABView)
appbuilder.add_view(GroupGeneralView(), "List Groups", icon="fa-folder-open-o", label=_('List Groups'),
                category="Contacts", category_icon='fa-envelope', category_label=_('Contacts'))
appbuilder.add_view(GroupMasterView(), "Master Detail Groups", icon="fa-folder-open-o",
                label=_("Master Detail Groups"), category="Contacts")
appbuilder.add_view(ContactGeneralView(), "List Contacts", icon="fa-envelope",
                label=_('List Contacts'), category="Contacts")
appbuilder.add_separator("Contacts")
appbuilder.add_view(ContactChartView(), "Contacts Chart", icon="fa-dashboard",
                label=_('Contacts Chart'), category="Contacts")
appbuilder.add_view(ContactTimeChartView(), "Contacts Birth Chart", icon="fa-dashboard",
                label=_('Contacts Birth Chart'), category="Contacts")

appbuilder.add_view_no_menu(ConfigView())

appbuilder.add_link(name="Cerulean", href="/config/themes/cerulean", icon="fa-external-link",
                category="Themes", category_label=_('Themes'))
appbuilder.add_link(name="Amelia", href="/config/themes/amelia", icon="fa-external-link", category="Themes")
appbuilder.add_link(name="Flatly", href="/config/themes/flatly", icon="fa-external-link", category="Themes")
appbuilder.add_link(name="Journal", href="/config/themes/journal", icon="fa-external-link", category="Themes")
appbuilder.add_link(name="Readable", href="/config/themes/readable", icon="fa-external-link", category="Themes")
appbuilder.add_link(name="Simplex", href="/config/themes/simplex", icon="fa-external-link", category="Themes")
appbuilder.add_link(name="Slate", href="/config/themes/slate", icon="fa-external-link", category="Themes")
appbuilder.add_link(name="Spacelab", href="/config/themes/spacelab", icon="fa-external-link", category="Themes")
appbuilder.add_link(name="United", href="/config/themes/united", icon="fa-external-link", category="Themes")
appbuilder.add_link(name="Default", href="/config/themes/default", icon="fa-external-link", category="Themes")
appbuilder.add_link(name="Reverse Menu", href="/config/navreverse", icon="fa-external-link")

