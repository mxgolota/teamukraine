from flask import Blueprint, render_template
from models import Club, ClubSpider, ClubMatches, ClubPlayers, UserExtended
from database import db_session, or_, join


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
def daily_matches_finished(club_id):
    club = Club.query.filter(Club.club_id == club_id).first()
    matches = ClubMatches.query\
        .filter(ClubMatches.status == 'finished')\
        .filter(ClubMatches.time_class == 'daily') \
        .filter(or_(ClubMatches.team1_id == club_id, ClubMatches.team2_id == club_id)) \
        .all()
    return render_template("daily_matches_finished.html", matches=matches, club=club)


@clubs_bp.route("/<int:club_id>/daily_matches_in_progress")
def daily_matches_in_progress(club_id):
    club = Club.query.filter(Club.club_id == club_id).first()
    matches = ClubMatches.query \
        .filter(ClubMatches.status == 'in_progress') \
        .filter(ClubMatches.time_class == 'daily') \
        .filter(or_(ClubMatches.team1_id == club_id, ClubMatches.team2_id == club_id)) \
        .all()

    return render_template("daily_matches_in_progress.html", matches=matches, club=club)


@clubs_bp.route("/<int:club_id>/daily_matches_registration")
def daily_matches_registration(club_id):
    club = Club.query.filter(Club.club_id == club_id).first()
    matches = ClubMatches.query \
        .filter(ClubMatches.status == 'registration') \
        .filter(ClubMatches.time_class == 'daily') \
        .filter(or_(ClubMatches.team1_id == club_id, ClubMatches.team2_id == club_id)) \
        .all()

    return render_template("daily_matches_registration.html", matches=matches, club=club)


@clubs_bp.route("/<int:club_id>/live_matches")
def live_matches(club_id):
    club = Club.query.filter(Club.club_id == club_id).first()
    matches = ClubMatches.query \
        .filter(or_(ClubMatches.team1_id == club_id, ClubMatches.team2_id == club_id)) \
        .filter(ClubMatches.time_class == 'live') \
        .order_by(ClubMatches.end_time.desc()) \
        .all()

    return render_template("live_matches.html", matches=matches, club=club)


@clubs_bp.route("/<int:club_id>/players")
def club_players(club_id):
    club = Club.query.filter(Club.club_id == club_id).first()
    players = UserExtended.query.join(ClubPlayers).filter(ClubPlayers.club_id == club_id).all()

    return render_template("club_players.html", club=club, players=players)
