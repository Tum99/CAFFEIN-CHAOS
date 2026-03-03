# seed_admin_menu.py
from app import create_app, db
from app.models import User, Category, Product
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# ----- Step 1: Create Admin -----
admin_email = "faithadmin@testing.com"
admin_password = "password123"

admin_user = User.query.filter_by(role='admin').first()
if not admin_user:
    admin_user = User(
        email=admin_email,
        password=generate_password_hash(admin_password, method="pbkdf2:sha256"),
        role="admin"
    )
    db.session.add(admin_user)
    db.session.commit()
    print(f"Admin created: {admin_email}")
else:
    print("Admin already exists")

# ----- Step 2: Create Categories -----
category_names = [
    "Fan Favourites",
    "Black Coffee",
    "Granito",
    "Flavoured Coffee",
    "Cold Coffee",
    "Speciality of Espresso",
    "Manual Brew",
    "Fruity Magnet",
    "Caffein Shake",
    "Sinful Cho Shake",
    "Hot Coffee",
    "Beverages"
    "Desserts"
]

for name in category_names:
    category = Category.query.filter_by(name=name).first()
    if not category:
        category = Category(name=name)
        db.session.add(category)
db.session.commit()
print("Categories added")

# ----- Step 3: Create Products -----
# Example structure: dictionary {category_name: [list of product dicts]}
products_data = {
    "Black Coffee": [
        {"name": "Dopio", "price": 250, "description": "Strong double espresso"},
        {"name": "Irish Coffee", "price": 350, "description": "Coffee with a touch of whiskey"},
        {"name": "Romana", "price": 200, "description": "Italian classic espresso"},
        {"name": "Americano", "price": 200, "description": "Italian classic espresso"},
        {"name": "Affogato", "price": 300, "description": "Italian classic espresso"},
        {"name": "Red Eye", "price": 300, "description": "Italian classic espresso"}
    ],
    "Granito": [
        {"name": "Mango Crush", "price": 700, "description": "Refreshing mango granita"},
        {"name": "Blue Curacao", "price": 700, "description": "Blue citrus icy drink"},
        {"name": "Kiwi Crush", "price": 700, "description": "Kiwi flavored icy delight"},
        {"name": "Strawberry Kiwi Tango", "price": 700, "description": "Italian classic espresso"},
        {"name": "Orange Crush", "price": 700, "description": "Italian classic espresso"},
        {"name": "Strawberry Orange Tango", "price": 700, "description": "Italian classic espresso"}
    ],
    "Flavoured Coffee": [
        {"name": "Nutty Milano", "price": 600, "description": "Hazelnut espresso"},
        {"name": "Caramel Classic", "price": 600, "description": "Caramel coffee delight"},
        {"name": "Espresso Madness", "price": 600, "description": "Double shot espresso with chocolate"},
        {"name": "Frozen Coffee Rum", "price": 600, "description": "Italian classic espresso"},
        {"name": "Cinamon Freeze", "price": 600, "description": "Italian classic espresso"},
        {"name": "Coffee Chocolate Shake", "price": 600, "description": "Italian classic espresso"}
        
    ],
    "Cold Coffee": [
        {"name": "Iced Mocha", "price": 500, "description": "Chocolate iced coffee"},
        {"name": "Caffein Frappe", "price": 600, "description": "Blended coffee frappe"},
        {"name": "Caffein Freeze", "price": 500, "description": "Frozen coffee drink"},
        {"name": "Iced Latte", "price": 500, "description": "Italian classic espresso"},
        {"name": "Iced Cappuchino", "price": 500, "description": "Italian classic espresso"},
        {"name": "Caffein Culture", "price": 500, "description": "Italian classic espresso"}
    ],

    "Manual Brew": [
        {"name": "Chemex Coffee", "price": 600, "description": "Chocolate iced coffee"},
        {"name": "Hario V60", "price": 600, "description": "Blended coffee frappe"},
        {"name": "Mocha Pot", "price": 600, "description": "Frozen coffee drink"},
        {"name": "French Press", "price": 600, "description": "Italian classic espresso"},
        {"name": "Siphon", "price": 800, "description": "Italian classic espresso"},
        {"name": "Aero Press", "price": 600, "description": "Italian classic espresso"}
    ],

    "Speciality of Espresso": [
        {"name": "Ristretto", "price": 250, "description": "Chocolate iced coffee"},
        {"name": "Espresso", "price": 250, "description": "Blended coffee frappe"},
        {"name": "Lungo", "price": 250, "description": "Frozen coffee drink"},
        {"name": "Flat White", "price": 300, "description": "Italian classic espresso"},
        {"name": "Cortado", "price": 300, "description": "Italian classic espresso"}
    ],

    "Fruity Magnet": [
        {"name": "Apple Pitch", "price": 600, "description": "Chocolate iced coffee"},
        {"name": "Strawberry Punch", "price": 600, "description": "Blended coffee frappe"},
        {"name": "Mango & Kiwi", "price": 600, "description": "Frozen coffee drink"},
        {"name": "Orange Dawa", "price": 600, "description": "Italian classic espresso"}
    ],

    "Beverages": [
        {"name": "Hot Lemon Ginger", "price": 300, "description": "Chocolate iced coffee"},
        {"name": "Pineapple Dawa", "price": 300, "description": "Blended coffee frappe"},
        {"name": "Hibiscus Dawa", "price": 300, "description": "Frozen coffee drink"},
        {"name": "Roibos Tea", "price": 300, "description": "Italian classic espresso"}
    ],

    "Sinful Cho Shake": [
        {"name": "Choco Chip Shake", "price": 750, "description": "Chocolate iced coffee"},
        {"name": "Kit Kat Shake", "price": 800, "description": "Blended coffee frappe"},
        {"name": "Oreo Shake", "price": 750, "description": "Frozen coffee drink"},
        {"name": "Bouborn Shake", "price": 800, "description": "Italian classic espresso"},
        {"name": "M & M Shake", "price": 800, "description": "Italian classic espresso"},
        {"name": "Ferro Rocher Shake", "price": 1000, "description": "Italian classic espresso"}
    ],

    "Caffein Shake": [
        {"name": "Caramel Shake", "price": 600, "description": "Chocolate iced coffee"},
        {"name": "Hezelnut Shake", "price": 600, "description": "Blended coffee frappe"},
        {"name": "Peppermint Shake", "price": 600, "description": "Frozen coffee drink"},
        {"name": "Fudge Milkshake", "price": 600, "description": "Italian classic espresso"},
        {"name": "Vanilla Milkshake", "price": 600, "description": "Italian classic espresso"},
        {"name": "Caffein Milkshake", "price": 600, "description": "Italian classic espresso"}
    ],

    "Hot Coffee": [
        {"name": "Macchiato", "price": 400, "description": "Chocolate iced coffee"},
        {"name": "Coffee Lite", "price": 450, "description": "Blended coffee frappe"},
        {"name": "Hot Chocolate", "price": 400, "description": "Frozen coffee drink"},
        {"name": "Cafe Latte", "price": 450, "description": "Italian classic espresso"},
        {"name": "Cappuchino", "price": 350, "description": "Italian classic espresso"},
        {"name": "Cafe Mocha", "price": 450, "description": "Italian classic espresso"}
    ],

    "Desserts": [
        {"name": "Caffein Addiction", "price": 500, "description": "Chocolate iced coffee"},
        {"name": "Caffein Madness", "price": 500, "description": "Blended coffee frappe"},
        {"name": "Caffein Temptation", "price": 500, "description": "Frozen coffee drink"},
        {"name": "Choco Brownie", "price": 1000, "description": "Italian classic espresso"},
        {"name": "Mochalito", "price": 500, "description": "Italian classic espresso"},
        {"name": "Caramelo", "price": 500, "description": "Italian classic espresso"}
    ]
    # Add other categories similarly to reach all 74 products
}

for cat_name, products in products_data.items():
    category = Category.query.filter_by(name=cat_name).first()
    if category:
        for p in products:
            existing = Product.query.filter_by(name=p["name"], category_id=category.id).first()
            if not existing:
                product = Product(
                    name=p["name"],
                    price=p["price"],
                    description=p["description"],
                    category_id=category.id
                )
                db.session.add(product)
db.session.commit()
print("Products added")

print("Seeding complete ✅")