from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required
from models import User, UserExtended, Events, Event_User
from datetime import datetime
from database import db_session
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
    form = PlayersCountDynamicsForm(request.form)
    if request.method == "GET":
        teams = [('1', 'Team 1'), ('2', 'Team 2')]
        form.team.choices = teams
        form.team.data = teams[0]
    return render_template('players_count_dynamics.html', form=form)
