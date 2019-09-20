from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from forms import RegisterForm, LoginForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
import uuid
import requests as r
import json


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, db.ForeignKey('players.username'))
    password = db.Column(db.String)

    info = db.relationship('UserExtended')


class UserExtended(db.Model):
    __tablename__ = 'players'
    username = db.Column(db.String, primary_key=True)
    url = db.Column(db.String)
    avatar = db.Column(db.String)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    conn = db.engine.raw_connection()
    cursor = conn.cursor()
    cursor.callproc("usp_stat_clubs_players_cnt")
    clubs_players_cnt = []
    for result in cursor.stored_results():
        for mid in result.fetchall():
            clubs_players_cnt.append(mid)
    conn.close()
    return render_template("index.html", clubs_players_cnt=clubs_players_cnt)


@app.route("/teams/<int:club_id>")
def club(club_id):
    conn = db.engine.raw_connection()
    info = conn.cursor()
    info.callproc("usp_club_info", [club_id])
    club_info = []
    for recordset in info.stored_results():
        for row in recordset:
            club_info.append(dict(zip(recordset.column_names, row)))
    info.close()

    matches = conn.cursor()
    matches.callproc("usp_club_matches", [club_id])
    club_matches = []
    for recordset in matches.stored_results():
        for row in recordset:
            club_matches.append(dict(zip(recordset.column_names, row)))
        matches.close()
    return render_template("club.html",
                           club_id=club_id,
                           club_info=club_info[0],
                           club_matches_reg=[x for x in club_matches if x['status'] == 'registration'],
                           club_matches_prog = [x for x in club_matches if x['status'] == 'in_progress'])

@app.route("/players")
def players():
    conn = db.engine.raw_connection()
    cursor = conn.cursor()
    cursor.callproc("usp_players_search")
    result = []
    for recordset in cursor.stored_results():
        for row in recordset:
            result.append(dict(zip(recordset.column_names, row)))
    cursor.close()
    return render_template("players.html", players=result)


@app.route("/tournaments/lcwl_u1600")
def lcwl_u1600():
    conn = db.engine.raw_connection()
    cursor = conn.cursor()
    cursor.callproc("usp_stat_lcwl_u1600")
    result = []
    for recordset in cursor.stored_results():
        for row in recordset:
            result.append(dict(zip(recordset.column_names, row)))
    cursor.close()

    points = pd.DataFrame(result)
    points = pd.pivot_table(points, columns=['club_2', 'round_id'], index=['player_1', 'chess_blitz_rating'], values='team1_player_score') \
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
    conn = db.engine.raw_connection()
    cursor = conn.cursor()
    cursor.callproc("usp_stat_lcwl_main")
    result = []
    for recordset in cursor.stored_results():
        for row in recordset:
            result.append(dict(zip(recordset.column_names, row)))
    cursor.close()

    points = pd.DataFrame(result)
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


@app.route("/tournaments/ucc2019")
@login_required
def ucc2019():
    conn = db.engine.raw_connection()
    cursor = conn.cursor()

    cursor.callproc("usp_stat_ucc2019_best_players")
    best_players_result = []
    for recordset in cursor.stored_results():
        for row in recordset:
            best_players_result.append(dict(zip(recordset.column_names, row)))

    cursor.callproc("usp_stat_ucc2019_rounds")
    rounds_result = []
    for recordset in cursor.stored_results():
        for row in recordset:
            rounds_result.append(dict(zip(recordset.column_names, row)))

    cursor.close()

    best_players = pd.DataFrame(best_players_result)
    rounds = pd.DataFrame(rounds_result)
    first_teams = rounds[['round_id', 'match_id', 'team1_name', 'team1_result', 'team2_name']]
    first_teams = first_teams.rename(columns={"team1_name": "team_name", "team1_result": "team_result", "team2_name": "opponent_name"})
    second_teams = rounds[['round_id', 'match_id', 'team2_name', 'team2_result', 'team1_name']]
    second_teams = second_teams.rename(columns={"team2_name": "team_name", "team2_result": "team_result", "team1_name": "opponent_name"})
    tournament_table = pd.concat([first_teams, second_teams]).reset_index()

    tournament_table = pd.pivot_table(tournament_table, columns=['opponent_name'], index=['team_name'], values='team_result').reset_index()

    tournament_table['Загалом'] = tournament_table.sum(axis=1)
    tournament_table.reset_index(inplace=True)

    return render_template("ucc2019.html", best_players=best_players, rounds=rounds, tournament_table=tournament_table)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    print(request.method)
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

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Ви усішно зареєстровані!', category='success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


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


if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run(debug=True)
