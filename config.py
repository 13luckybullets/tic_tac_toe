# Set configurations of SQLAlchemy


class Configuration(object):
    debug = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:1488@localhost/game_db'
