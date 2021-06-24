from flask import Flask, request, abort, jsonify, redirect, render_template, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()

def init_app():
	app = Flask(__name__)
	app.config.from_object('config.DevConfig')
	#db.init_app(app)


	#with app.app_context():
		# Import parts of our application
		#db.create_all()
	from app.ftp import bp as ftp_bp
	app.register_blueprint(ftp_bp)

		#db.create_all()



	return app
	