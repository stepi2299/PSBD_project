from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_uploads import configure_uploads, patch_request_class, UploadSet, IMAGES

app = Flask(__name__)
app.config.from_object(Config)
config = app.config
login = LoginManager(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

from app import views
