from flask import Blueprint, render_template
from database import db_session, or_, join, engine
import pandas as pd
import json
import numpy as np


dashboards_bp = Blueprint('dashboards_bp', __name__, template_folder='templates', url_prefix='/dashboards')


@dashboards_bp.route('/')
def index():
    return render_template('dashboards.html')


@dashboards_bp.route('/tu_hq_rm_dasboard/')
def tu_hq_rm_dasboard():
    with engine.connect() as conn:
        result = conn.execute("call team_ukraine_in_progress_matches_dashboard")
        in_progress_matches_result = [row for row in result]
        in_progress_matches_columns = result.keys()

    in_progress_matches = pd.DataFrame(in_progress_matches_result, columns=in_progress_matches_columns)

    leagues = in_progress_matches['match_type'].unique()

    return render_template('tu_hq_rm_dasboard.html', in_progress_matches=in_progress_matches, leagues=leagues)


@dashboards_bp.route('/team_dnipro_dashboard/')
def team_dnipro_dashboard():
    with engine.connect() as conn:
        result = conn.execute("call team_dnipro_dashboard")
        in_progress_matches_result = [row for row in result]
        in_progress_matches_columns = result.keys()

    in_progress_matches = pd.DataFrame(in_progress_matches_result, columns=in_progress_matches_columns)
    return render_template(
        'team_dnipro_dashboard.html',
        ecl2020=in_progress_matches[in_progress_matches['match_type'] == 'ECL2020'],
        altw=in_progress_matches[in_progress_matches['match_type'] == 'All around the World'],
        other=in_progress_matches[in_progress_matches['match_type'] == 'Other'],)


@dashboards_bp.route("/tu_lcel")
def lcel_s1():
    with engine.connect() as conn:
        result = conn.execute("call usp_stat_lcel_s1_rounds")
        rounds_result = [row for row in result]
        rounds_result_columns = result.keys()

    rounds = pd.DataFrame(rounds_result, columns=rounds_result_columns)
    first_teams = rounds[['round_id', 'match_id', 'team1_id', 'team1_result', 'team2_id']]
    first_teams = first_teams.rename(columns={"team1_id": "team_name", "team1_result": "team_result", "team2_id": "opponent_name"})
    second_teams = rounds[['round_id', 'match_id', 'team2_id', 'team2_result', 'team1_id']]
    second_teams = second_teams.rename(columns={"team2_id": "team_name", "team2_result": "team_result", "team1_id": "opponent_name"})
    tournament_table = pd.concat([first_teams, second_teams]).reset_index()

    tournament_table = tournament_table.groupby(['team_name', 'opponent_name'])['team_result'].sum(min_count=1).unstack().reset_index()

    print(tournament_table)

    tournament_table['Загалом'] = tournament_table.iloc[:, 2:].sum(axis=1)
    # tournament_table[tournament_table[0]].astype('int')
    print(tournament_table)
    tournament_table.reset_index(inplace=True)
    tournament_table.sort_values(by=['Загалом'], ascending=False, inplace=True)

    return render_template("tu_lcel_dashboard.html", rounds=rounds, tournament_table=tournament_table)


@dashboards_bp.route('/tu_hq_reg_dashboard/')
def tu_hq_reg_dashboard():
    with engine.connect() as conn:
        result = conn.execute("call team_ukraine_reg_matches_dashboard")
        reg_matches_result = [row for row in result]
        reg_matches_columns = result.keys()

    matches = pd.DataFrame(reg_matches_result, columns=reg_matches_columns)
    return render_template('tu_hq_reg_dashboard.html', matches=matches)


@dashboards_bp.route('/crimea_reg_dashboard/')
def crimea_reg_dashboard():
    with engine.connect() as conn:
        result = conn.execute("call team_crimea_reg_matches_dashboard")
        reg_matches_result = [row for row in result]
        reg_matches_columns = result.keys()

    matches = pd.DataFrame(reg_matches_result, columns=reg_matches_columns)
    return render_template('tu_hq_reg_dashboard.html', matches=matches)