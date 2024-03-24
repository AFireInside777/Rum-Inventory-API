from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, login_manager, ma 
from config import Config
from helpers import JSONEncoder

from .site.routes import site
from .authentication.routes import auth
from .api.routes import api

app = Flask(__name__)

CORS(app)
app.config.from_object(Config)
app.json_encoder = JSONEncoder
db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db, compare_type=True)

app.register_blueprint(site) #/home
app.register_blueprint(auth) #signup
app.register_blueprint(api)