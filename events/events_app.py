from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required
from models import User, UserExtended, Events, Event_User
from datetime import datetime
from database import db_session
from .forms import EventUpdateForm
from flask_login import current_user


events_bp = Blueprint('events_bp', __name__, template_folder='templates', url_prefix='/events')


@events_bp.route('/')
def index():
    actual_events = Events.query.filter(Events.event_date >= datetime.utcnow().date()).order_by(Events.event_date)
    previous_events = Events.query.filter(Events.event_date < datetime.utcnow().date()).order_by(Events.event_date)
    return render_template('events.html', actual_events=actual_events, previous_events=previous_events)


@events_bp.route('/<int:event_id>')
def event(event_id):
    this_event = Events.query.filter_by(event_id=event_id).first()
    if this_event is None:
        abort(404)
    return render_template('event_page.html', this_event=this_event)


@login_required
@events_bp.route('/add_event', methods=["GET", "POST"])
def add_event():
    if not current_user.rights.can_edit_events == 1:
        return abort(403)
    create_form = EventUpdateForm(request.form)
    if request.method == "GET":
        return render_template('event_create_page.html', create_form=create_form)

    new_event = Events(event_name=request.form.get("event_name"),
                       event_description=request.form.get("event_description"),
                       event_date=request.form.get("event_date"))
    db_session.add(new_event)
    db_session.commit()
    return redirect(url_for("events_bp.index"))


@login_required
@events_bp.route("/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id):
    this_event = Events.query.filter_by(event_id=event_id).first()

    if this_event is None:
        abort(404)
    if not current_user.rights.can_edit_events == 1:
        return abort(403)

    update_form = EventUpdateForm(request.form)

    update_form.event_name.data = this_event.event_name
    update_form.event_description.data = this_event.event_description
    update_form.event_date.data = this_event.event_date

    if request.method == "GET":
        return render_template("event_update_page.html", event=this_event, update_form=update_form)

    this_event.event_name = request.form.get("event_name")
    this_event.event_description = request.form.get("event_description")
    # this_event.event_name = request.form.get("event_name")
    this_event.event_date = request.form.get("event_date")

    db_session.commit()
    return redirect(url_for("events_bp.index"))


@login_required
@events_bp.route("/<int:event_id>/delete", methods=["GET", "POST"])
def delete_event(event_id):
    this_event = Events.query.filter_by(event_id=event_id).first()
    
    if this_event is None:
        abort(404)
    if not current_user.rights.can_edit_events == 1:
        return abort(403)

    db_session.delete(this_event)
    db_session.commit()
    return redirect(url_for("events_bp.index"))
