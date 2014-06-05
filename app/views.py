import calendar
from flask import render_template, redirect
from flask.ext.appbuilder.models.datamodel import SQLAModel
from flask.ext.appbuilder.models.group import aggregate_avg, aggregate_sum
from flask.ext.appbuilder.views import MasterDetailView, ModelView
from flask.ext.appbuilder.baseviews import expose, BaseView
from flask.ext.appbuilder.charts.views import ChartView, TimeChartView, DirectByChartView, GroupByChartView
from flask.ext.babelpkg import lazy_gettext as _

from app import db, appbuilder
from models import Group, Gender, Contact, CountryStats, Country


class ContactModelView(ModelView):
    datamodel = SQLAModel(Contact)

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
    label_columns = ContactModelView.label_columns
    group_by_columns = ['group', 'gender']
    datamodel = SQLAModel(Contact)


class ContactTimeChartView(TimeChartView):
    chart_title = 'Grouped Birth contacts'
    chart_type = 'AreaChart'
    label_columns = ContactModelView.label_columns
    group_by_columns = ['birthday']
    datamodel = SQLAModel(Contact)


class GroupModelView(ModelView):
    datamodel = SQLAModel(Group)
    related_views = [ContactModelView]
    #show_template = 'appbuilder/general/model/show_cascade.html'


class ConfigView(BaseView):
    route_base = "/config"

    @expose('/themes/<string:theme>')
    def index(self, theme=''):
        if theme == "default":
            self.appbuilder.app_theme = ''
        else:
            self.appbuilder.app_theme = "%s.css" % (theme)
        return redirect(self._get_redirect())

    @expose('/navreverse/')
    def navreverse(self):
        self.appbuilder.menu.reverse = not self.appbuilder.menu.reverse
        return redirect(self._get_redirect())


class GroupMasterView(MasterDetailView):
    datamodel = SQLAModel(Group)
    related_views = [ContactModelView]

#-----------------------------------------------------
#-----------------------------------------------------

def pretty_month_year(value):
    return calendar.month_name[value.month] + ' ' + str(value.year)

def pretty_year(value):
    return str(value.year)


class CountryStatsModelView(ModelView):
    datamodel = SQLAModel(CountryStats)
    list_columns = ['country', 'stat_date', 'population', 'unemployed', 'college']
    base_permissions = ['can_list', 'can_show']


class CountryDirectChartView(DirectByChartView):
    datamodel = SQLAModel(CountryStats)
    chart_title = 'Direct Data Chart Example'

    definitions = [
        {
            #'label': 'Monthly',
            'group': 'stat_date',
            'series': ['unemployed',
                       'college']
        }
    ]


class CountryGroupByChartView(GroupByChartView):
    datamodel = SQLAModel(CountryStats)
    chart_title = 'Grouped Data Example'

    definitions = [
        {
            'label': 'Country Stat',
            'group': 'country',
            'series': [(aggregate_avg, 'unemployed'),
                       (aggregate_avg, 'population'),
                       (aggregate_avg, 'college')
            ]
        },
        {
            'label': 'Monthly',
            'group': 'month_year',
            'formatter': pretty_month_year,
            'series': [(aggregate_sum, 'unemployed'),
                       (aggregate_avg, 'population'),
                       (aggregate_avg, 'college')
            ]
        },
        {
            'label': 'Yearly',
            'group': 'year',
            'formatter': pretty_year,
            'series': [(aggregate_sum, 'unemployed'),
                       (aggregate_avg, 'population'),
                       (aggregate_avg, 'college')
            ]
        }
    ]


class CountryPieGroupByChartView(GroupByChartView):
    datamodel = SQLAModel(CountryStats)
    chart_title = 'Grouped Data Example (Pie)'
    chart_type = 'PieChart'

    definitions = [
        {
            'label': 'Country Stat',
            'group': 'country',
            'series': [(aggregate_avg, 'unemployed')
            ]
        }
    ]


class MasterGroupByChartView(MasterDetailView):
    datamodel = SQLAModel(Country)
    base_order = ('name','asc')
    related_views = [CountryDirectChartView]


appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", label=_('List Groups'),
                category="Contacts", category_icon='fa-envelope', category_label=_('Contacts'))
appbuilder.add_view(GroupMasterView, "Master Detail Groups", icon="fa-folder-open-o",
                label=_("Master Detail Groups"), category="Contacts")
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope",
                label=_('List Contacts'), category="Contacts")
appbuilder.add_separator("Contacts")
appbuilder.add_view(ContactChartView, "Contacts Chart", icon="fa-dashboard",
                label=_('Contacts Chart'), category="Contacts")
appbuilder.add_view(ContactTimeChartView, "Contacts Birth Chart", icon="fa-dashboard",
                label=_('Contacts Birth Chart'), category="Contacts")


appbuilder.add_view(CountryStatsModelView, "Chart Data (Country)", icon="fa-globe",
                label=_('Chart Data (Country)'), category_icon="fa-dashboard", category="Chart Examples")
appbuilder.add_view(CountryDirectChartView, "Direct Chart Example", icon="fa-bar-chart-o",
                label=_('Direct Chart Example'), category="Chart Examples")
appbuilder.add_view(MasterGroupByChartView, "Master Chart Example", icon="fa-bar-chart-o",
                label=_('Master Detail Chart Example'), category="Chart Examples")
appbuilder.add_view(CountryGroupByChartView, "Group By Chart Example", icon="fa-bar-chart-o",
                label=_('Group By Chart Example'), category="Chart Examples")
appbuilder.add_view(CountryPieGroupByChartView, "Group By Pie Chart Example", icon="fa-bar-chart-o",
                label=_('Group By Pie Chart Example'), category="Chart Examples")


appbuilder.add_view_no_menu(ConfigView)

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

