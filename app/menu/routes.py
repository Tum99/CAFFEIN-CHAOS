from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Category, Product

menu = Blueprint('menu', __name__)

@menu.route('/menu/')
# @login_required
def main_menu():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template(
        "menu/menu.html",
        categories=categories,
        products=products
    )
    
