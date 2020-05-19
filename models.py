import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, default='Guest')
    last_name = db.Column(db.String, default=random.randint(1000, 9999))
    birthdate = db.Column(db.DATE)
    phone_number = db.Column(db.String)
    institution = db.Column(db.String)
    address_1 = db.Column(db.String)
    address_2 = db.Column(db.String)
    joined_date = db.Column(db.DATE, default=datetime.today().strftime('%Y-%m-%d'))


class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    time_access = db.Column(db.Integer, default=0)

class UserStatus(db.Model):
    __tablename__ = "userstatus"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
    day_left = db.Column(db.Integer)

class Content(db.Model):
    __tablename__ = "contents"
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.VARCHAR)
    