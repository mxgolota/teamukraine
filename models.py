from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base, db_session


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey('players.username'))
    password = Column(String)
    liked = relationship('Event_User', foreign_keys='Event_User.user_id', backref='user', lazy='dynamic')

    info = relationship('UserExtended')

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
    username = Column(String, primary_key=True)
    url = Column(String)
    avatar = Column(String)


class Events(Base):
    __tablename__ = 'chess_events'
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String)
    event_short_description = Column(String)
    event_description = Column(String)
    event_picture = Column(String)
    event_date = Column(DateTime)
    submits = relationship('Event_User', backref='chess_events', lazy='dynamic')


class Event_User(Base):
    __tablename__ = 'chess_events_users'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('chess_events.event_id'))
    user_id = Column(Integer, ForeignKey('users.id'))
