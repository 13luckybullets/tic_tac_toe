from app import db
from datetime import datetime


class Game(db.Model):
    __tablename__ = 'Game'

    id = db.Column(db.Integer, primary_key=True)
    field_size = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now())
    winner = db.Column(db.String(140))

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<id:{self.id}, field:{ self.field_size}X{ self.field_size}, date:{self.date}>'


class GameLog(db.Model):
    __tablename__ = 'GameLog'

    id = db.Column(db.Integer, primary_key=True)
    move = db.Column(db.Integer)
    line = db.Column(db.Integer)
    point = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super(GameLog, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<id:{self.id}>'