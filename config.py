import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

project_dir = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(project_dir, "orders.db"))

    MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID')
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL')
    MQTT_BROKER_PORT = os.environ.get('MQTT_BROKER_PORT')
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
    MQTT_TLS_ENABLED = os.environ.get('MQTT_TLS_ENABLED')

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    MQTT_BROKER_PORT = os.environ.get('MQTT_BROKER_PORT')
    MQTT_ORDER_TOPIC = os.environ.get('MQTT_ORDER_TOPIC')
    MQTT_QOS = os.environ.get('MQTT_QOS')

    DOWNLOADED_DIRECTORY = os.path.join(basedir, os.environ.get('DOWNLOAD_FOLDER'))
    UPLOAD_DIRECTORY = os.path.join(basedir,os.environ.get('UPLOAD_FOLDER'))
    ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    #DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    #environ.get('DEV_DATABASE_URI')