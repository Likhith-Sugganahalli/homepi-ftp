import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

project_dir = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')

    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(project_dir, "orders.db"))

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    MQTT_BROKER_PORT = os.environ.get('MQTT_BROKER_PORT')
    MQTT_ORDER_TOPIC = os.environ.get('MQTT_ORDER_TOPIC')
    MQTT_QOS = os.environ.get('MQTT_QOS')

    DOWNLOADED_DIRECTORY = os.path.join(basedir, os.environ.get('DOWNLOAD_FOLDER'))
    UPLOAD_DIRECTORY = os.path.join(basedir,os.environ.get('UPLOAD_FOLDER'))
    ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS')

    FLASK_ENV='development'

    DEBUG = os.environ.get('DEBUG')
    TESTING = os.environ.get('TESTING')

    #ENV = "development"
    #FLASK_DEBUG=1