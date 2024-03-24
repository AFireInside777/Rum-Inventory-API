from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from flask_login import UserMixin, LoginManager
import secrets
from flask_marshmallow import Marshmallow
from datetime import datetime
from werkzeug.security import generate_password_hash

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, unique=True, default='')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, password):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f'User {self.email} has been added as a User for the app. They may login with their password.'
    
class Rum(db.Model): #You have to provide the Company, name and price
    rum_id = db.Column(db.String(150), primary_key = True)
    rum_company = db.Column(db.String(150), nullable = False)
    rum_name = db.Column(db.String(150), nullable = False)
    rum_age = db.Column(db.String(150), nullable = True, default = "0 Years")
    rum_stock_qty = db.Column(db.Integer(), nullable = True, default = 0)
    rum_price = db.Column(db.Float(), nullable = False, default = 0.00)
    rum_user_token = db.Column(db.String(150), nullable = False)

    def __init__(self, rum_company, rum_name, rum_stock_qty, rum_price, rum_user_token, rum_age="0 Years"):
        self.rum_id = self.set_rum_id()
        self.rum_company = rum_company
        self.rum_name = rum_name
        self.rum_stock_qty = rum_stock_qty
        self.rum_price = rum_price
        self.rum_user_token = rum_user_token
        self.rum_age = rum_age
        
    
    def set_rum_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f'A Rum entry has been added for: {self.rum_company} {self.rum_name}'
    
class RumSchema(ma.Schema):
    class Meta:
        fields = ['rum_id', 'rum_company', 'rum_name', 'rum_price', 'rum_age']

rum_schema = RumSchema()
rums_schema = RumSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'email', 'g_auth_verify', 'token', 'date_created']

user_schema = UserSchema()
users_schema = UserSchema(many=True)