from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_uploads import configure_uploads, UploadSet, IMAGES

app = Flask(__name__)
app.config.from_object(Config)
config = app.config
login = LoginManager(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from app import views
