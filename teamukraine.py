from flask import Flask, render_template, flash, redirect, url_for, logging, request
from forms import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import uuid
import requests as r
import json
from models import User, Events
from database import db_session, engine
from datetime import datetime
from events.events_app import events_bp
from admin.admin_app import admin_bp
from clubs.clubs_app import clubs_bp
from dashboards.dashboards_app import dashboards_bp
from tournaments.tournaments_app import tournaments_bp


app = Flask(__name__)
app.config.from_object('config.Config')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    app.register_blueprint(events_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(clubs_bp)
    app.register_blueprint(dashboards_bp)
    app.register_blueprint(tournaments_bp)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


@app.route("/")
def index():
    last_events = Events.query.filter(Events.event_date >= datetime.utcnow().date()).order_by(Events.event_date)
    return render_template("index.html", last_events=last_events)


@app.route('/tu_best_daily_players_2020/')
def tu_best_daily_players_dashboard():
    with engine.connect() as conn:
        result = conn.execute("call tu_best_daily_players_dashboard")
        best_players_result = [row for row in result]
        best_players_columns = result.keys()

    best_players = pd.DataFrame(best_players_result, columns=best_players_columns)
    return render_template('tu_best_daily_players_dashboard.html', best_players=best_players)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'GET':
        form.secret_key.data = str(uuid.uuid4())

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = generate_password_hash(form.password.data, method='sha256')
        secret_key = form.secret_key.data

        if User.query.filter_by(username=form.username.data).first() is not None:
            flash('Цей користувач вже зареєстрований', category='danger')
            return redirect(url_for('register'))

        player_location = json.loads(r.get('https://api.chess.com/pub/player/{}'.format(username)).text)
        if 'location' not in player_location:
            flash('Такого користувача не існує на chess.com', category='danger')
            return redirect(url_for('register'))
        if player_location['location'] != secret_key:
            flash('Не співпадає секретний ключ', category='danger')
            return redirect(url_for('register'))

        user = User(username=username, password=password, role_id=3)
        db_session.add(user)
        db_session.commit()

        flash('Ви усішно зареєстровані!', category='success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/register_help')
def register_help():
    return render_template('register_help.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':

        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Привіт!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильний логін або пароль', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('До зустрічі!', 'success')
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('profile.html', user=user)


@app.route('/submit_event/<int:event_id>/')
@login_required
def submit_event_action(event_id):
    event = Events.query.filter_by(event_id=event_id).first()
    current_user.submit_to_event(event)
    return redirect(request.referrer)


if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run(debug=True)