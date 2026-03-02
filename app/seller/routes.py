from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import SellerProfile, DirectMessage
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

@seller.route('/dashboard')
@login_required
@seller_required
def dashboard():
    return render_template('seller/dashboard.html')

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
