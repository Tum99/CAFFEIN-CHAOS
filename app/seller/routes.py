from flask import render_template
from app.seller import seller

@seller.route('/seller/dashboard')
def seller_dashboard():
    return render_template('seller/dashboard.html')

@seller.route('/seller/listings')
def seller_listings():
    return "Seller listings page"

@seller.route('/seller/respond/<int:request_id>')
def respond_to_request(request_id):
    return f"Respond to buyer request {request_id}"
