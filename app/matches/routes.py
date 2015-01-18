from flask import render_template, current_app, request, url_for
from . import matches
from .. import updates, db
from ..models import User, Match, Message, Photo


@matches.route('/')
def index():
  # Update db
  updates.update()

  #page = request.args.get('page', 1, type=int)
  #pagination = User.query.order_by(User.id.desc()).paginate(page, per_page = current_app.config['CHATS_PER_PAGE'], error_out=False)
  #user_list = pagination.items

  user_list = User.query.order_by(User.last_active.desc()).limit(50).all()
  user_list = user_list[1:]
  for user in user_list:
    user.last_active = user.last_active.strftime('%I:%M %p, %B %d')
    match = Match.query.filter_by(user_id_2=user.id).first()
    user.num_msgs = Message.query.filter_by(match_id=match.match_id).count()

  return render_template('matches/index.html', users=user_list)
#, pagination=pagination)


@matches.route('/user/<id>')
def user(id):
  # Query for user account
  usr = User.query.filter_by(id=id).first()
  # Get the match
  match = Match.query.filter_by(user_id_2=id).first()
  # Get all the messages and sort by timestamp
  msgs = Message.query.filter_by(match_id=match.match_id).all()
  #msgs = msgs.order_by(Message.timestamp.desc())
  photos = Photo.query.filter_by(user_id=id).all()

  return render_template('matches/user.html',user=usr,photos=photos,msgs=msgs)

