from flask import render_template, redirect, url_for
from app.buyer import buyer

@buyer.route('/buyer/dashboard')
def buyer_dashboard():
    return render_template('buyer/dashboard.html')

@buyer.route('/buyer/orders')
def buyer_orders():
    return "Buyer Orders Page"

@buyer.route('/buyer/post-request')
def post_request():
    return "Page for buyers to post order requests/bids"
