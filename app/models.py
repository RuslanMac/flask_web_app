from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(128), index=True, unique=True)
	email = db.Column(db.String(128), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
	languages = db.relationship('Dictionary', backref='user', lazy='dynamic')


	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))



class Word(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	native_language=db.Column(db.String(128))
	foreign_language=db.Column(db.String(128))
	remarks=db.Column(db.String(128))
	level=db.Column(db.Integer, default=1)
	dictionary_id=db.Column(db.Integer,db.ForeignKey('dictionary.id'))

	def __repr__(self):
		return '<Word {}>'.format(self.native_language)


	def serialize(self):
		return {
		'foreign_language': self.foreign_language,
		'native_language': self.native_language
		}

class Language(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	language = db.Column(db.String(128))
	lit = db.Column(db.String(4))
	users = db.relationship('User', backref='language', lazy='dynamic')

	def __repr__(self):
		return '<Language {}>'.format(self.language)


class Dictionary(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
	words = db.relationship('Word', backref='dictionary', lazy='dynamic')


	def __repr__(self):
		return '<Dictionary {}, user_id {}, language_id {}>'.format(self.id, self.user_id, self.language_id)








