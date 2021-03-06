import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask import request
from logging.handlers import RotatingFileHandler

import os
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
bootstrap = Bootstrap(app)
babel = Babel(app)
from app import routes, models

if not app.debug:
	if not os.path.exists('logs1'):
		os.mkdir('logs1')
	file_handler = RotatingFileHandler('logs1/lang.log', maxBytes=10240,
												backupCount=10)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.setLevel(logging.INFO)
	app.logger.info('Lang startup')

@babel.localeselector
def get_locale():
	return request.accept_languages.best_match(app.config['LANGUAGES'])