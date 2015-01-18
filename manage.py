#!/usr/bin/env python
import os, json, datetime, dateutil.parser
from flask import escape
from app import create_app
from flask.ext.script import Manager
from sqlalchemy import text
from app import db
from app.models import User, Match, Message, Photo

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def adduser(id, match_id, name, bio):
    """Register a new user."""
    db.create_all()
    user = User(id=id, match_id=match_id,name=name,bio=bio)
    db.session.add(user)
    db.session.commit()

@manager.command
def load_db(update_data):
  data = json.load(open(update_data))

  me = '54b1f298028d748a414fb24d'
  
  #print( json.dumps(data['matches'][0], indent=4) )

  db.create_all()

  u1 = None
  # If I am already in db, get that entry for first user
  if User.query.filter_by(id=me).count() == 1:
    u1 = User.query.filter_by(id=me).first()
  else:     # OW we need to make a me entry
    u1 = User(id=me, name='ME', bio='')
    db.session.add(u1)
    db.session.commit()

  # Iterate matches
  for match in data['matches']:
    if 'messages' in match and 'person' in match:

      #print( User.query.filter_by(id=me).all() )

      uid2 = match['person']['_id']
      # Check that the user doesn't already exist
      if User.query.filter_by(id=uid2).count() > 0 or me == uid2:
        print('There was a collision on', uid2)
        continue
      last_active = dateutil.parser.parse(match['messages'][-1]['sent_date'])
      thumb = match['person']['photos'][0]['processedFiles'][3]['url']
      u2 = User(id=uid2,name=match['person']['name'],bio=match['person']['bio'],last_active=last_active,thumb_url=thumb)
      db.session.add(u2)

      # Create Match
      mid = match['_id']
      # Check that there isn't an identical message
      if Match.query.filter_by(match_id=mid).count() > 0:
        print('There was a collision on', mid)
        continue

      m = Match(match_id=mid, user_id_1=me, user_id_2=uid2)
      db.session.add(m)

      # Make messages
      for msg in match['messages']:
        body = text(msg['message'])
        timestamp = datetime.datetime.fromtimestamp(msg['timestamp']/1000.0)
        author_id = str(u2.id)
        if msg['from'] == me:
          author_id = me
        else:
          author_id = str(u2.id)

        msg = Message(match_id=mid,body=str(body),timestamp=timestamp, user_id=author_id)
        db.session.add(msg)

      # Add photos
      for photo in match['person']['photos']:
        url = photo['processedFiles'][0]['url']
        if Photo.query.filter_by(url=url).count() > 0:
          print('There was a collision on', mid)
          continue
        pht = Photo(user_id=uid2, url=url)
        db.session.add(pht)

  db.session.commit()



if __name__ == '__main__':
    manager.run()

