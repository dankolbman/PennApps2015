from datetime import datetime
from . import db


# Users hold our matches with their info and conversations
class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.String(64), primary_key=True)
  name = db.Column(db.String(64), nullable=False)
  bio = db.Column(db.Text())
  #match = db.relationship('Match', lazy='dynamic', backref='matcher')
  #match = db.Column(db.String(64), db.ForeignKey('matches.match_id'))
  

class Match(db.Model):
  __tablename__  = 'matches'
  match_id = db.Column(db.String(64), primary_key=True)
  user_id_1 = db.Column(db.String(64), db.ForeignKey('users.id'))
  user_id_2 = db.Column(db.String(64), db.ForeignKey('users.id'))

# Holds a message that is part of a users conversation with us
class Message(db.Model):
  __tablename__ = 'messages'
  id = db.Column(db.Integer, primary_key=True)
  match_id = db.Column(db.String(256), db.ForeignKey('matches.match_id'))
  body = db.Column(db.Text)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)
  user_id = db.Column(db.String(100), db.ForeignKey('users.id'))
  
  def __str__(self):
    return str(self.body)

