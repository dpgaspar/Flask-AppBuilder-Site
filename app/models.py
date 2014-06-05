import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from flask.ext.appbuilder.models.mixins import AuditMixin, BaseMixin, FileColumn, ImageColumn
from flask.ext.appbuilder import Model


class Group(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    group = relationship("Group")
    gender_id = Column(Integer, ForeignKey('gender.id'), nullable=False)
    gender = relationship("Gender")

    def __repr__(self):
        return self.name

    def month_year(self):
        return datetime.datetime(self.birthday.year, self.birthday.month, 1)

    def year(self):
        return datetime.datetime(self.birthday.year, 1, 1)


#----------------------------------------------------------
#  Chart Views Example
#----------------------------------------------------------


class Country(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class CountryStats(Model):
    id = Column(Integer, primary_key=True)
    stat_date = Column(Date, nullable=True)
    population = Column(Float)
    unemployed = Column(Float)
    college = Column(Float)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    country = relationship("Country")

    def __repr__(self):
        return "{0}:{1}:{2}:{3}".format(self.stat_date, self.country, self.population, self.college)

    def month_year(self):
        return datetime.datetime(self.stat_date.year, self.stat_date.month, 1)

    def year(self):
        return datetime.datetime(self.stat_date.year,1, 1)
