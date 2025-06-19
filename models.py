from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('shop_name', db.String, db.ForeignKey('shop.name'), primary_key=True)  # ← 外部キーを追加！
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    favorites = db.relationship('Shop', secondary=favorites, backref='liked_by')  # ← 追加

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Shop(db.Model):
    name = db.Column(db.String, primary_key=True)
    area = db.Column(db.String)
