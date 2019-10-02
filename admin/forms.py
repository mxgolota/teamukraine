from wtforms import Form, StringField, TextAreaField, validators, SelectField
from wtforms.fields.html5 import DateTimeLocalField


class PlayersCountDynamicsForm(Form):
    begin_date = DateTimeLocalField('Дата початку', format='%Y-%m-%d')
    end_date = DateTimeLocalField('Дата закінчення', format='%Y-%m-%d')
    team = SelectField('Команда')
