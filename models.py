from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from database import Base, db_session


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey('players.username'))
    password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    liked = relationship('Event_User', foreign_keys='Event_User.user_id', backref='user', lazy='dynamic')
    info = relationship('UserExtended')
    rights = relationship('UserRoles')

    def submit_to_event(self, event):
        if not self.submitted_to_event(event):
            submit = Event_User(user_id=self.id, event_id=event.event_id)
            db_session.add(submit)
            db_session.commit()
        else:
            Event_User.query.filter_by(user_id=self.id, event_id=event.event_id).delete()
            db_session.commit()

    def submitted_to_event(self, event):
        result = Event_User.query.filter(Event_User.user_id == self.id, Event_User.event_id == event.event_id).count() > 0
        return result


class UserExtended(Base):
    __tablename__ = 'players'
    player_id = Column(Integer)
    username = Column(String, primary_key=True)
    url = Column(String)
    avatar = Column(String)
    chess_bullet_rating = Column(Integer)
    chess_blitz_rating = Column(Integer)
    chess_rapid_rating = Column(Integer)
    chess_daily_rating = Column(Integer)
    chess_daily_timeout_percent = Column(DECIMAL)
    clubs = relationship('ClubPlayers', backref='players')


class UserRoles(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String)
    can_change_users_roles = Column(Integer)
    can_edit_events = Column(Integer)
    can_access_to_admin_page = Column(Integer)


class Events(Base):
    __tablename__ = 'chess_events'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String)
    event_short_description = Column(String)
    event_description = Column(String)
    event_picture = Column(String)
    event_date = Column(DateTime)
    important = Column(Integer)
    submits = relationship('Event_User', backref='chess_events', lazy='dynamic')


class Event_User(Base):
    __tablename__ = 'chess_events_users'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('chess_events.event_id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    event_user = relationship('User', backref='chess_events_users')


class Club(Base):
    __tablename__ = 'clubs'
    club_id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    created = Column(DateTime)
    join_request = Column(String)
    description = Column(String)
    url = Column(String)
    info = relationship('ClubSpider')
    players = relationship('ClubPlayers', backref='clubs')
    matches = relationship('ClubMatches', primaryjoin="or_(Club.club_id==ClubMatches.team1_id, Club.club_id==ClubMatches.team2_id)", lazy='dynamic')


class ClubSpider(Base):
    __tablename__ = 'clubs_spider'
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)
    gather_full_info = Column(Integer)


class ClubPlayers(Base):
    __tablename__ = 'pl_cl'
    # id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'), primary_key=True)
    club_id = Column(Integer, ForeignKey('clubs.club_id'), primary_key=True)
    player_info = relationship('UserExtended')


class ClubMatches(Base):
    __tablename__ = 'matches'
    match_id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String)
    boards = Column(Integer)
    rules = Column(Integer)
    time_class = Column(String)
    time_control = Column(String)
    team1_id = Column(Integer, ForeignKey('clubs.club_id'))
    team1_score = Column(DECIMAL)
    team2_id = Column(Integer, ForeignKey('clubs.club_id'))
    team2_score = Column(DECIMAL)
    min_rating = Column(Integer)
    max_rating = Column(Integer)
    team1 = relationship('Club', primaryjoin='Club.club_id==ClubMatches.team1_id')
    team2 = relationship('Club', primaryjoin='Club.club_id==ClubMatches.team2_id')
