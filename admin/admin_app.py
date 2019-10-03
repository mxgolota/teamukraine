from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required
from models import User, UserExtended, Events, Event_User
from datetime import datetime, timedelta
from database import db_session, engine
from flask_login import current_user
from .forms import PlayersCountDynamicsForm

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', url_prefix='/admin')


@admin_bp.route('/reporting')
@login_required
def reporting():
    if not current_user.rights.can_access_to_admin_page:
        abort(403)
    return render_template('reporting.html')


@admin_bp.route('/reporting/players_count_dynamics', methods=['GET', 'POST'])
@login_required
def rep_players_count_dynamics():
    if not current_user.rights.can_access_to_admin_page:
        abort(403)
    form = PlayersCountDynamicsForm(request.form)
    with engine.connect() as conn:
        result = conn.execute("call usp_rep_players_count_dynamics_filt_teams")
        teams = [row for row in result]
        form.team.choices = teams

    if request.method == "GET":
        form.begin_date.data = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=-7)
        form.end_date.data = datetime.now().replace(hour=0, minute=0, second=0)
        return render_template('players_count_dynamics.html', form=form)

    if request.method == 'POST':
        team_id = form.team.data
        begin_date = form.begin_date.data.date()
        end_date = form.end_date.data.date()

    with engine.connect() as conn:
        result = conn.execute("call usp_rep_players_count_dynamics(%s, %s, %s)", (team_id, begin_date, end_date))
        result_table = [row for row in result]

        dates = [date['fulldate'].strftime("%d/%m/%Y") for date in result_table]
        values = [value['players_cnt'] for value in result_table]

    return render_template('players_count_dynamics.html', form=form, dates=dates, values=values)
