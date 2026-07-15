from datetime import datetime
from extensions import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    watch_requests = db.relationship(
        "WatchRequest",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Product(db.Model):
    __tablename__ = "products"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255),nullable=False)
    url=db.Column(db.Text,unique=True,nullable=False)
    website=db.Column(db.String(60))
    current_price=db.Column(db.Float,nullable=False)
    image_url=db.Column(db.Text)
    last_checked=db.Column(db.DateTime)
    watch_requests = db.relationship(
        "WatchRequest",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    price_history = db.relationship(
        "PriceHistory",
        back_populates="product",
        cascade="all, delete-orphan"
    )

class WatchRequest(db.Model):
    __tablename__="watch_requests"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey("products.id"),nullable=False)
    target_price=db.Column(db.Float,nullable=False)
    notification_sent=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    user = db.relationship(
        "User",
        back_populates="watch_requests"
    )
    product = db.relationship(
        "Product",
        back_populates="watch_requests"
    )

class PriceHistory(db.Model):
    __tablename__ = "price_history"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )
    price = db.Column(db.Float, nullable=False)
    checked_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    product = db.relationship(
        "Product",
        back_populates="price_history"
    )