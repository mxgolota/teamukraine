from flask import Blueprint, render_template
from database import db_session, or_, join, engine
import pandas as pd

dashboards_bp = Blueprint('dashboards_bp', __name__, template_folder='templates', url_prefix='/dashboards')


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

    leagues = in_progress_matches['match_type'].unique()

    return render_template('team_dnipro_dashboard.html', in_progress_matches=in_progress_matches, leagues=leagues)


@dashboards_bp.route('/tu_hq_reg_dashboard/')
def tu_hq_reg_dashboard():
    with engine.connect() as conn:
        result = conn.execute("call team_ukraine_reg_matches_dashboard")
        reg_matches_result = [row for row in result]
        reg_matches_columns = result.keys()

    with engine.connect() as conn:
        result = conn.execute("call team_ukraine_reg_matches_dashboard_timeouts")
        timeouts_result = [row for row in result]
        timeouts_columns = result.keys()

    with engine.connect() as conn:
        result = conn.execute("call team_ukraine_reg_matches_dashboard_mobilization")
        mobilization_result = [row for row in result]
        mobilization_columns = result.keys()

    matches = pd.DataFrame(reg_matches_result, columns=reg_matches_columns)
    timeouts = pd.DataFrame(timeouts_result, columns=timeouts_columns)
    mobilization = pd.DataFrame(mobilization_result, columns=mobilization_columns)
    mobilization_ukraine = mobilization[mobilization['team_name'] == 'Team Ukraine']
    mobilization_opponent = mobilization[mobilization['team_name'] != 'Team Ukraine']

    mobilization_ukraine['avg_rating'] = mobilization_ukraine['avg_rating'].astype(int)
    mobilization_opponent['avg_rating'] = mobilization_opponent['avg_rating'].astype(int)

    # {{ mobilization['fulldate'].tolist() }}
    return render_template('tu_hq_reg_dashboard.html', matches=matches, timeouts=timeouts,
                           mobilization_ukraine=mobilization_ukraine,
                           mobilization_opponent=mobilization_opponent)


@dashboards_bp.route('/kyiv_hq_reg_dashboard/')
def kyiv_reg_dashboard():
    with engine.connect() as conn:
        result = conn.execute("call kyiv_reg_matches_dashboard")
        reg_matches_result = [row for row in result]
        reg_matches_columns = result.keys()

    with engine.connect() as conn:
        result = conn.execute("call kyiv_reg_matches_dashboard_timeouts")
        timeouts_result = [row for row in result]
        timeouts_columns = result.keys()

    matches = pd.DataFrame(reg_matches_result, columns=reg_matches_columns)
    timeouts = pd.DataFrame(timeouts_result, columns=timeouts_columns)
    return render_template('kyiv_reg_dashboard.html', matches=matches, timeouts=timeouts)


@dashboards_bp.route('/crimea_hq_reg_dashboard/')
def crimea_reg_dashboard():
    with engine.connect() as conn:
        result = conn.execute("call crimea_reg_matches_dashboard")
        reg_matches_result = [row for row in result]
        reg_matches_columns = result.keys()

    with engine.connect() as conn:
        result = conn.execute("call crimea_reg_matches_dashboard_timeouts")
        timeouts_result = [row for row in result]
        timeouts_columns = result.keys()

    matches = pd.DataFrame(reg_matches_result, columns=reg_matches_columns)
    timeouts = pd.DataFrame(timeouts_result, columns=timeouts_columns)
    return render_template('crimea_reg_dashboard.html', matches=matches, timeouts=timeouts)


@dashboards_bp.route('/tu_best_daily_players_dashboard/')
def tu_best_daily_players_dashboard():
    with engine.connect() as conn:
        result = conn.execute("call tu_best_daily_players_dashboard")
        best_players_result = [row for row in result]
        best_players_columns = result.keys()

    best_players = pd.DataFrame(best_players_result, columns=best_players_columns)
    return render_template('tu_best_daily_players_dashboard.html', best_players=best_players)


@dashboards_bp.route('/tu_hq_players_count_dashboard/')
def tu_hq_players_count_dashboard():
    with engine.connect() as conn:
        result = conn.execute("call usp_dashboards_Ukraine_vs_Russia_playersCount")
        players_result = [row for row in result]
        players_columns = result.keys()

    players = pd.DataFrame(players_result, columns=players_columns)
    return render_template('tu_hq_players_count_dashboard.html', players=players)


@dashboards_bp.route('/team_dnipro_carousel/')
def team_dnipro_carousel():
    return render_template('team_dnipro_carousel.html')
