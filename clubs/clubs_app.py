from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required
from models import User, UserExtended, Events, Event_User, Club, ClubSpider, ClubMatches
from datetime import datetime
from database import db_session
from flask_login import current_user


clubs_bp = Blueprint('clubs_bp', __name__, template_folder='templates', url_prefix='/clubs')


@clubs_bp.route('/')
def index():
    clubs = Club.query.join(ClubSpider).filter(ClubSpider.gather_full_info == 1)
    return render_template('clubs.html', clubs=clubs)


@clubs_bp.route("/<int:club_id>")
def club_index(club_id):
    club = Club.query.filter(Club.club_id == club_id).first()

    return render_template("club.html", club=club)

@clubs_bp.route("/<int:club_id>/daily_matches_finished")
def club_index(club_id):
    matches = ClubMatches.query\
        .filter(ClubMatches.team1 == club_id or ClubMatches.team2 == club_id)\
        .filter(ClubMatches.status == 'finished')\
        .all()

    return render_template("club.html", club=club)
