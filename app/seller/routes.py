from flask import flash, Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import SellerProfile, DirectMessage, FarmProfile, Product, FarmProductListing, GrowerBuyerTransaction
from app.utils.decorators import seller_required
from datetime import datetime
from app import db

seller = Blueprint('seller', __name__, url_prefix='/seller')


@seller.route('/setup', methods=['GET', 'POST'])
@login_required
@seller_required
def seller_setup():
    farm = FarmProfile.query.filter_by(user_id=current_user.id).first()
    if farm and farm.is_setup_complete:
        pass

    my_listings = []
    if farm:
        my_listings = FarmProductListing.query.filter_by(farm_id=farm.id).all()

    steps = 0
    if farm: steps += 1
    if len(my_listings) > 0: steps += 1

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
        whatsapp_phone = request.form.get('whatsapp')
        profile_image = request.form.get('farm_photo')

        if not farm:
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
                is_verified=False,
                is_setup_complete=False,
                phone=phone,
                whatsapp_phone=whatsapp_phone
            )
            db.session.add(farm)
            db.session.commit()

        flash('Farm profile created! Now add your first listing.', 'success')
        # After setup — go straight to the real dashboard
        return redirect(url_for('seller.seller_setup'))

    return render_template(
        'seller/new_seller.html',
        farm=farm,
        body_class='page-setup',
        active_page='dashboard',
        listings=my_listings,
        total_steps=steps 
    )



@seller.route('/dashboard')
@login_required
@seller_required
def dashboard():
    # Check if this seller has a farm profile yet and any listings
    farm = FarmProfile.query.filter_by(user_id=current_user.id).first()

    if not farm or not farm.is_setup_complete:
        return redirect(url_for('seller.seller_setup'))

    elif farm:
        orders = GrowerBuyerTransaction.query.filter_by(grower_id=current_user.id).all()
    else:
        orders = []

    # 1. Get all completed/paid transactions
    completed_orders = [o for o in orders if o.status in ['paid', 'completed']]

    # 2. Calculate earnings per product
    product_earnings = {}
    for order in completed_orders:
        name = order.product.name
        product_earnings[name] = product_earnings.get(name, 0) + order.total_amount

    # 3. Calculate Commission (5%)
    total_gross = sum(product_earnings.values())
    commission = total_gross * 0.05
    net_earnings = total_gross - commission

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
        total_gross=total_gross,
        commission=commission,
        net_earnings=net_earnings,
        is_new_seller=(farm is None),  # ← True if brand new
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


@seller.route('/add-listing', methods=['POST'])
@login_required
@seller_required
def add_listing():
    # 1. Fetch the Farm Profile first (we need farm.id)
    farm = FarmProfile.query.filter_by(user_id=current_user.id).first()
    if not farm:
        flash("Please complete your Farm Profile first!", "error")
        return redirect(url_for('seller.seller_setup'))

    # 2. Create the General Product Entry
    # This matches your 'class Product' model
    master_product = Product(
        seller_id=current_user.id,
        name=request.form.get('name'),
        description=request.form.get('description'),
        price=float(request.form.get('price', 0)),
        stock=int(request.form.get('stock', 0)),
        product_type='farm'
    )
    
    db.session.add(master_product)
    db.session.flush()  # This 'pushes' the product to get an ID without committing yet

    # Grab data from the 'name' attributes in HTML
    product_name = request.form.get('name')
    price = request.form.get('price')
    stock = request.form.get('stock')
    
    # 3. Create the Detailed Farm Listing
    # This matches your 'class FarmProductListing' model
    farm_listing = FarmProductListing(
        product_id=master_product.id, # Link it to the Product we just made
        farm_id=farm.id,
        varietal=request.form.get('varietal'),
        process=request.form.get('process'),
        roast_level=request.form.get('roast'),
        quantity_kg=float(request.form.get('stock', 0)),
        price_per_kg=float(request.form.get('price', 0)),
        tasting_notes=request.form.get('notes'),
        minimum_order_kg=float(request.form.get('min_order', 1.0))
    )

    # Handle the Harvest Date (string to date object)
    harvest_date_str = request.form.get('harvest_date')
    if harvest_date_str:
        farm_listing.harvest_date = datetime.strptime(harvest_date_str, '%Y-%m-%d').date()
    
    db.session.add(farm_listing)
    db.session.commit()

    flash('Listing published! Step 2 complete.', 'success')
    return redirect(url_for('seller.seller_setup'))


@seller.route('/listings')
@login_required
@seller_required
def listings():
    farm = FarmProfile.query.filter_by(user_id=current_user.id).first()
    my_listings = FarmProductListing.query.filter_by(farm_id=farm.id)\
                  .order_by(FarmProductListing.listed_at.desc()).all()

    # --- ADD THIS LOGIC ---
    # Calculate steps for the progress bar in new_seller.html
    steps_done = 0
    if farm:
        steps_done += 1 # Step 1: Farm Profile
    if len(my_listings) > 0:
        steps_done += 2 # Step 2: First Listing (adds to the total)
        # Note: adjust this logic based on how you want to count 3 steps total
    
    return render_template('seller/new_seller.html', 
                           farm=farm, 
                           listings=my_listings,
                           total_steps=steps_done) # <--- Pass total_steps here!