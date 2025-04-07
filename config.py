# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///mrzoo.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "2404@Theo")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "2404@Theo")
