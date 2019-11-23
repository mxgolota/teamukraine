from flask import Flask, render_template, flash, redirect, url_for, logging, request
from forms import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
import uuid
import requests as r
import json
from models import User, Events
from database import db_session, engine
from datetime import datetime
from events.events_app import events_bp
from admin.admin_app import admin_bp
from clubs.clubs_app import clubs_bp


app = Flask(__name__)
app.config.from_object('config.Config')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    app.register_blueprint(events_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(clubs_bp)


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


@app.route("/tournaments/lcwl_u1600")
def lcwl_u1600():
    with engine.connect() as conn:
        tmp = conn.execute("call usp_stat_lcwl_u1600")
        result = [row for row in tmp]
        columns = tmp.keys()

    points = pd.DataFrame(result, columns=columns)
    points = pd.pivot_table(points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_score') \
        .reset_index()
    cols = [('player_1', ''), ('chess_blitz_rating', '')] + sorted(list(points.columns)[2:], key=lambda x: x[1])
    points = points.reindex(columns=cols).reset_index(drop=True)

    points['Total'] = points[list(points.columns[2:])].sum(axis=1)
    rivals = points.columns[2:]
    points = points.sort_values(by=['Total'], ascending=False)
    points['Place'] = np.arange(1, len(points) + 1)

    return render_template("lcwl_best_players.html", points=points, rivals=rivals)


@app.route("/tournaments/lcwl_main")
def lcwl_main():
    with engine.connect() as conn:
        tmp = conn.execute("call usp_stat_lcwl_main")
        result = [row for row in tmp]
        columns = tmp.keys()

    points = pd.DataFrame(result, columns=columns)
    max_points = pd.DataFrame(result, columns=columns)
    points = pd.pivot_table(points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_score') \
        .reset_index()
    cols = [('player_1', ''), ('chess_blitz_rating', '')] + sorted(list(points.columns)[2:], key=lambda x: x[1])
    points = points.reindex(columns=cols).reset_index(drop=True)

    points['Total'] = points[list(points.columns[2:])].sum(axis=1)
    rivals = points.columns[2:]
    points = points.sort_values(by=['Total'], ascending=False)
    points['Place'] = np.arange(1, len(points) + 1)

    max_points = pd.pivot_table(max_points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'],
                            values='team1_player_max_possible_score').reset_index()
    max_points = max_points.reindex(columns=cols).reset_index(drop=True)

    max_points['Total_max'] = max_points[list(max_points.columns[2:])].sum(axis=1)

    points = pd.merge(points, max_points[['Total_max', 'player_1']], on='player_1', how='left')
    points['points_percentage'] = 100*points['Total']/points['Total_max']
    points = points.sort_values(by=['Total', 'points_percentage'], ascending=False)

    return render_template("lcwl_best_players.html", points=points, rivals=rivals)


@app.route("/tournaments/ucc2019")
def ucc2019():
    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2019_best_players")
        best_players_result = [row for row in result]
        best_players_columns = result.keys()

    with engine.connect() as conn:
        result = conn.execute("call usp_stat_ucc2019_rounds")
        rounds_result = [row for row in result]
        rounds_result_columns = result.keys()

    best_players = pd.DataFrame(best_players_result, columns=best_players_columns)
    rounds = pd.DataFrame(rounds_result,columns=rounds_result_columns)
    first_teams = rounds[['round_id', 'match_id', 'team1_name', 'team1_result', 'team2_name']]
    first_teams = first_teams.rename(columns={"team1_name": "team_name", "team1_result": "team_result", "team2_name": "opponent_name"})
    second_teams = rounds[['round_id', 'match_id', 'team2_name', 'team2_result', 'team1_name']]
    second_teams = second_teams.rename(columns={"team2_name": "team_name", "team2_result": "team_result", "team1_name": "opponent_name"})
    tournament_table = pd.concat([first_teams, second_teams]).reset_index()

    tournament_table = pd.pivot_table(tournament_table, columns=['opponent_name'], index=['team_name'], values='team_result').reset_index()

    tournament_table['Загалом'] = tournament_table.sum(axis=1)
    tournament_table.reset_index(inplace=True)
    tournament_table.sort_values(by=['Загалом'], ascending=False, inplace=True)

    return render_template("ucc2019.html", best_players=best_players, rounds=rounds, tournament_table=tournament_table)


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