pybabel extract -F ./babel/babel.cfg -k lazy_gettext -o ./babel/messages.pot app
pybabel update -N -i ./babel/messages.pot -d app/translations
pybabel compile -d app/translations


