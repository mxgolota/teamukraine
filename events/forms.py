from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, validators
from wtforms.fields.html5 import DateTimeLocalField


class EventUpdateForm(Form):
    event_name = StringField('Назва події', [validators.Length(min=3, max=100)])
    event_description = TextAreaField('Опис події', [validators.Length(min=10)])
    event_date = DateTimeLocalField('Дата початку події', format='%Y-%m-%dT%H:%M')
