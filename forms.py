from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, validators


class LoginForm(Form):
    username = StringField('Логін')
    password = PasswordField('Пароль')
    remember = BooleanField('Запам"ятати мене')


class RegisterForm(Form):
    username = StringField('Логін з chess.com', [validators.Length(min=3, max=100)])
    password = PasswordField('Пароль', [
        validators.Length(min=6),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Паролі не збігаються')
    ])
    confirm = PasswordField('Підвтердіть, будь-ласка, пароль')
    secret_key = StringField('Секретний ключ', render_kw={'readonly': True})
