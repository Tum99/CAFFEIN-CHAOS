# app/models.py
from datetime import datetime
from flask_login import UserMixin
from app import db


# Users (buyers, sellers, and admin)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'buyer', 'seller' or 'admin'

    # Relationships
    products = db.relationship(
        'Product',
        backref='seller', 
        lazy=True
        )

    services = db.relationship(
        'Service', 
        backref='seller', 
        lazy=True
        )

    messages_sent = db.relationship(
        'DirectMessage',
        foreign_keys='DirectMessage.sender_id',
        backref='sender',
        lazy=True
    )

    messages_received = db.relationship(
        'DirectMessage',
        foreign_keys='DirectMessage.receiver_id',
        backref='receiver',
        lazy=True
    )

    seller_profile = db.relationship(
        "SellerProfile",
        backref="user",
        uselist=False
    )

    buyer_profile = db.relationship(
        "BuyerProfile",
        backref="user",
        uselist=False
    )

    def __repr__(self):
        return f"<User {self.email}>"

    

class SellerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))

    def __repr__(self):
        return f"<SellerProfile {self.user_id}>"


class BuyerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    preferences = db.Column(db.Text)

    def __repr__(self):
        return f"<BuyerProfile {self.user_id}>"


# Products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=1)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    # Relationship: each product has many images
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product {self.name}>"


#Product Catehory
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    products = db.relationship("Product", backref="category", lazy=True)


#Product Image
class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    image_path = db.Column(db.String(255), nullable=False)
    # example: "uploads/products/image_1234.jpg"

    def __repr__(self):
        return f"<ProductImage {self.id} for Product {self.product_id}>"

#Cart Items
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, default=1)



# Services
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    category = db.Column(db.String(50))  # e.g., 'drink', 'repair'
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ServiceBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='pending')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Messages
class DirectMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Reviews
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    target_type = db.Column(db.String(20))  # 'product' or 'service'
    target_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(255))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer_profile.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bids = db.relationship("Bid", backref="request", lazy=True)


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profile.id'))
    offer_price = db.Column(db.Float)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    ingredients = db.Column(db.Text)
    steps = db.Column(db.Text)
    category = db.Column(db.String(50))  # e.g., cold brew, latte, espresso

