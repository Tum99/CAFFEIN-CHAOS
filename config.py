import os

class Config:
    SECRET_KEY = "Next3ig$tar!"  # change this later
    SQLALCHEMY_DATABASE_URI = "mysql://username:password@localhost/caffein_chaos"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
