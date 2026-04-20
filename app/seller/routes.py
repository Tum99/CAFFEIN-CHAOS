from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import SellerProfile, DirectMessage, FarmProfile, Product, FarmProductListing
from app.utils.decorators import seller_required

seller = Blueprint('seller', __name__, url_prefix='/seller')


@seller.route('/seller')
@login_required
@seller_required
def profile():
    return render_template(
        'seller/profile.html',
        seller=current_user.seller_profile
    )

@seller.route('/dashboard/seller')
@login_required
@seller_required
def dashboard():
    # Check if this seller has a farm profile yet and any listings
    farm = FarmProfile.query.filter_by(user_id=current_user.id).first()
    listings = Product.query.filter_by(
        seller_id=current_user.id,
        product_type='farm'
    ).all() if farm else []

    return render_template('seller/dashboard.html',
        active_page='dashboard',
        body_class='page-dashboard',
        farm=farm,
        listings=listings,
        is_new_seller=farm is None,  # ← True if brand new
        has_listings=len(listings) > 0
        )

@seller.route('/<int:seller_id>')
@login_required
def public_profile(seller_id):
    seller_profile = SellerProfile.query.get_or_404(seller_id)

    return render_template(
        'seller/public_profile.html',
        seller=seller_profile
    )

@seller.route('/messages')
@login_required
@seller_required
def messages():
    # Get messages sent TO this seller
    messages = DirectMessage.query.filter_by(
        receiver_id=current_user.id
    ).order_by(DirectMessage.timestamp.desc()).all()

    return render_template(
        'seller/messages.html',
        messages=messages
    )
