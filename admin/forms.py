from wtforms import Form, SelectField
from wtforms.fields.html5 import DateTimeLocalField


class PlayersCountDynamicsForm(Form):
    begin_date = DateTimeLocalField('Дата початку', format='%Y-%m-%dT%H:%M')
    end_date = DateTimeLocalField('Дата закінчення', format='%Y-%m-%dT%H:%M')
    team = SelectField('Команда')


class ClubsMembershipChangesForm(Form):
    begin_date = DateTimeLocalField('Дата початку', format='%Y-%m-%dT%H:%M')
    end_date = DateTimeLocalField('Дата закінчення', format='%Y-%m-%dT%H:%M')
    team = SelectField('Команда')

