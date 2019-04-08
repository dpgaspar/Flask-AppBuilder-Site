import datetime
import random
import logging
from . import db
from .models import Gender, Country, CountryStats

log = logging.getLogger(__name__)


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()


def fill_data():
    countries = ['Portugal', 'Germany', 'Spain', 'France', 'USA', 'China', 'Russia', 'Japan']
    for country in countries:
        c = Country(name=country)
        try:
            db.session.add(c)
            db.session.commit()
        except Exception as e:
            log.error("Update ViewMenu error: {0}".format(str(e)))
            db.session.rollback()
    try:
        data = db.session.query(CountryStats).all()
        if len(data) == 0:
            for x in range(1, 40):
                cs = CountryStats()
                cs.population = random.randint(1, 100)
                cs.unemployed = random.randint(1, 100)
                cs.college = random.randint(1, 100)
                year = random.choice(range(1900, 2012))
                month = random.choice(range(1, 12))
                day = random.choice(range(1, 28))
                cs.stat_date = datetime.datetime(year, month, day)
                cs.country_id = random.randint(1, len(countries))
                db.session.add(cs)
                db.session.commit()
    except Exception as e:
        log.error("Update Data error: {0}".format(str(e)))
        db.session.rollback()
