from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate



import pymysql


# Make PyMySQL act as MySQLdb
pymysql.install_as_MySQLdb()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()


# Redirect unauthorized users to login page
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app import models

    # Register blueprints
    from app.main.routes import main
    from app.auth.routes import auth
    from app.services.routes import services
    from app.buyer.routes import buyer
    from app.seller.routes import seller
    from app.events.routes import events
    from app.products.routes import products
    from app.general.routes import general

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(services)
    app.register_blueprint(buyer)
    app.register_blueprint(seller)
    app.register_blueprint(events)
    app.register_blueprint(products)
    app.register_blueprint(general)

    @app.route('/test-products')
    def test_products():
        return "Products route is alive"


    return app


# Flask-Login user loader
from app.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
