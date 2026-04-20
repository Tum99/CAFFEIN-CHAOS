from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import SellerProfile, DirectMessage, FarmProfile, Product, FarmProductListing
from app.utils.decorators import seller_required

seller = Blueprint('seller', __name__, url_prefix='/seller')


@seller.route('setup/seller')
@login_required
@seller_required
def seller_setup():
    farm = FarmProfile.query.filter_by(user_id=current_user.id).first()
    if farm:
        return redirect(url_for('seller_dashboard'))

    if request.method == 'POST':
        # Read form data
        farm_name    = request.form.get('farm_name')
        county       = request.form.get('county')
        location     = request.form.get('location')
        farm_size    = request.form.get('farm_size')
        altitude     = request.form.get('altitude')
        certifications = request.form.get('certifications')
        bio          = request.form.get('bio')
        phone        = request.form.get('phone')

        # Create the FarmProfile
        farm = FarmProfile(
            user_id=current_user.id,
            farm_name=farm_name,
            county=county,
            location=location,
            farm_size_acres=float(farm_size) if farm_size else None,
            altitude_masl=int(altitude) if altitude else None,
            certifications=certifications,
            bio=bio,
            is_verified=False
        )
        db.session.add(farm)
        db.session.commit()

        flash('Farm profile created! Now add your first listing.', 'success')
        # After setup — go straight to the real dashboard
        return redirect(url_for('seller.dashboard'))

    return render_template(
        'seller/new_seller.html',
        body_class='page-setup',
        active_page='dashboard'
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
    orders   = []
    earnings = 0

    if farm:
        listings = Product.query.filter_by(
            seller_id=current_user.id,
            product_type='farm'
        ).all()

        orders = GrowerBuyerTransaction.query.filter_by(
            grower_id=current_user.id
        ).order_by(GrowerBuyerTransaction.created_at.desc()).all()

        earnings = sum(
            t.total_amount for t in orders
            if t.status in ['paid', 'completed']
        )

    return render_template('seller/dashboard.html',
        active_page='dashboard',
        body_class='page-dashboard',
        farm=farm,
        listings=listings,
        orders=orders,
        earnings=earnings,
        is_new_seller=farm is None,  # ← True if brand new
        has_listings=len(listings) > 0,
        has_orders=len(orders) > 0
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
