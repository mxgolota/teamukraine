from wtforms import Form, StringField, TextAreaField, validators, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime


class PlayersCountDynamicsForm(Form):
    begin_date = DateTimeLocalField('Дата початку', format='%Y-%m-%dT%H:%M')
    end_date = DateTimeLocalField('Дата закінчення', format='%Y-%m-%dT%H:%M')
    team = SelectField('Команда')
