from flask import Flask, request, abort, jsonify, redirect, render_template, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging

#db = SQLAlchemy()

def init_app(config_class = Config):
	app = Flask(__name__)
	logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
	app.config.from_object(config_class)
	#db.init_app(app)
	app.logger.info(app.config)


	#with app.app_context():
		# Import parts of our application
		#db.create_all()
	from app.ftp import bp as ftp_bp
	app.register_blueprint(ftp_bp)

		#db.create_all()



	return app
	