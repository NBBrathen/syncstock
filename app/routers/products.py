from typing import List
from fastapi import APIRouter, HTTPException

from app.schemas import Product, ProductCreate, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

fake_products_db: List[Product] = [
    # Fruits & Vegetables
    Product(id=1, name="organic gala apple", price=0.99, stock=155),
    Product(id=2, name="banana", price=0.59, stock=210),
    Product(id=3, name="navel orange", price=1.29, stock=88),
    Product(id=4, name="red seedless grapes (lb)", price=3.49, stock=45),
    Product(id=5, name="strawberries (1 lb)", price=4.99, stock=32),
    Product(id=6, name="blueberries (pint)", price=5.29, stock=58),
    Product(id=7, name="iceberg lettuce", price=2.19, stock=40),
    Product(id=8, name="carrots (2 lb bag)", price=2.99, stock=75),
    Product(id=9, name="broccoli crown", price=2.49, stock=60),
    Product(id=10, name="russet potatoes (5 lb bag)", price=4.50, stock=90),
    Product(id=11, name="yellow onion", price=0.89, stock=120),
    Product(id=12, name="garlic bulb", price=0.79, stock=180),
    Product(id=13, name="hass avocado", price=2.50, stock=77),
    Product(id=14, name="tomato on the vine", price=2.99, stock=55),
    Product(id=15, name="cucumber", price=1.19, stock=65),
    Product(id=16, name="green bell pepper", price=1.49, stock=82),
    Product(id=17, name="baby spinach (5 oz)", price=3.99, stock=38),
    Product(id=18, name="lemon", price=0.99, stock=115),
    Product(id=19, name="lime", price=0.89, stock=130),
    Product(id=20, name="celery stalks", price=2.29, stock=48),
    # Pantry Staples
    Product(id=21, name="long-grain white rice (2 lb)", price=3.99, stock=105),
    Product(id=22, name="spaghetti pasta (16 oz)", price=1.99, stock=150),
    Product(id=23, name="all-purpose flour (5 lb)", price=4.29, stock=65),
    Product(id=24, name="granulated sugar (4 lb)", price=3.79, stock=80),
    Product(id=25, name="sea salt grinder", price=3.19, stock=95),
    Product(id=26, name="black peppercorn grinder", price=3.19, stock=92),
    Product(id=27, name="extra virgin olive oil (500ml)", price=9.99, stock=70),
    Product(id=28, name="vegetable oil (48 oz)", price=5.49, stock=60),
    Product(id=29, name="canned diced tomatoes (14.5 oz)", price=1.59, stock=250),
    Product(id=30, name="canned black beans (15 oz)", price=1.29, stock=300),
    Product(id=31, name="creamy peanut butter (16 oz)", price=4.49, stock=110),
    Product(id=32, name="clover honey (12 oz)", price=6.99, stock=55),
    Product(id=33, name="soy sauce (10 oz)", price=3.29, stock=85),
    Product(id=34, name="distilled white vinegar (32 oz)", price=2.99, stock=75),
    Product(id=35, name="old-fashioned rolled oats (18 oz)", price=4.99, stock=100),
    Product(id=36, name="honey nut breakfast cereal", price=4.79, stock=98),
    Product(id=37, name="ground coffee (12 oz)", price=8.99, stock=120),
    Product(id=38, name="black tea bags (100 ct)", price=5.29, stock=140),
    Product(id=39, name="ketchup (20 oz)", price=3.59, stock=115),
    Product(id=40, name="yellow mustard (14 oz)", price=2.49, stock=130),
    # Dairy & Eggs
    Product(id=41, name="whole milk (gallon)", price=4.89, stock=50),
    Product(id=42, name="sharp cheddar cheese block (8 oz)", price=4.29, stock=68),
    Product(id=43, name="mozzarella cheese shredded (8 oz)", price=4.29, stock=72),
    Product(id=44, name="greek yogurt, plain (32 oz)", price=6.49, stock=45),
    Product(id=45, name="salted butter (1 lb)", price=5.99, stock=80),
    Product(id=46, name="large brown eggs (dozen)", price=4.99, stock=95),
    Product(id=47, name="heavy whipping cream (pint)", price=3.99, stock=35),
    Product(id=48, name="sour cream (16 oz)", price=2.99, stock=48),
    Product(id=49, name="cottage cheese (24 oz)", price=4.19, stock=30),
    Product(id=50, name="cream cheese (8 oz)", price=3.49, stock=66),
    # Meat & Seafood
    Product(id=51, name="boneless chicken breast (lb)", price=6.99, stock=62),
    Product(id=52, name="ground beef 85/15 (lb)", price=5.99, stock=55),
    Product(id=53, name="new york strip steak (lb)", price=14.99, stock=25),
    Product(id=54, name="pork chops (lb)", price=4.99, stock=40),
    Product(id=55, name="sliced bacon (12 oz)", price=7.99, stock=70),
    Product(id=56, name="atlantic salmon fillet (lb)", price=12.99, stock=33),
    Product(id=57, name="raw shrimp, peeled (lb)", price=11.99, stock=28),
    Product(id=58, name="tilapia fillet (lb)", price=8.99, stock=36),
    Product(id=59, name="hot dogs (8 pack)", price=4.50, stock=99),
    Product(id=60, name="deli-sliced turkey (lb)", price=9.49, stock=22),
    # Bakery
    Product(id=61, name="classic white bread", price=3.29, stock=50),
    Product(id=62, name="100% whole wheat bread", price=3.49, stock=45),
    Product(id=63, name="plain bagels (6 ct)", price=4.19, stock=30),
    Product(id=64, name="chocolate chip cookies (12 ct)", price=5.99, stock=40),
    Product(id=65, name="blueberry muffins (4 ct)", price=5.49, stock=28),
    # Frozen Foods
    Product(id=66, name="pepperoni rising crust pizza", price=7.99, stock=60),
    Product(id=67, name="frozen mixed vegetables (16 oz)", price=2.79, stock=85),
    Product(id=68, name="vanilla bean ice cream (1.5 qt)", price=6.49, stock=70),
    Product(id=69, name="frozen waffles (10 ct)", price=3.99, stock=55),
    Product(id=70, name="crispy fish sticks (24 oz)", price=8.99, stock=42),
    # Snacks
    Product(id=71, name="classic potato chips", price=4.29, stock=110),
    Product(id=72, name="pretzels", price=3.49, stock=90),
    Product(id=73, name="microwave popcorn (3 ct)", price=3.19, stock=130),
    Product(id=74, name="cheddar cheese crackers", price=3.99, stock=105),
    Product(id=75, name="chewy granola bars (6 ct)", price=4.49, stock=88),
    Product(id=76, name="roasted almonds (16 oz)", price=9.99, stock=60),
    Product(id=77, name="milk chocolate bar", price=1.99, stock=200),
    Product(id=78, name="beef jerky (3 oz)", price=6.99, stock=48),
    # Beverages
    Product(id=79, name="bottled spring water (24 pack)", price=5.99, stock=150),
    Product(id=80, name="cola (12 pack)", price=8.99, stock=120),
    Product(id=81, name="lemon-lime soda (2 liter)", price=2.49, stock=95),
    Product(id=82, name="orange juice (64 oz)", price=4.79, stock=70),
    Product(id=83, name="apple juice (64 oz)", price=3.99, stock=75),
    Product(id=84, name="iced tea (gallon)", price=3.29, stock=45),
    Product(id=85, name="energy drink (16 oz)", price=2.99, stock=180),
    # Household Items
    Product(id=86, name="paper towels (6 rolls)", price=9.99, stock=90),
    Product(id=87, name="toilet paper (12 mega rolls)", price=14.99, stock=110),
    Product(id=88, name="dish soap (28 oz)", price=4.49, stock=85),
    Product(id=89, name="laundry detergent (100 oz)", price=15.99, stock=70),
    Product(id=90, name="tall kitchen trash bags (80 ct)", price=12.99, stock=65),
    Product(id=91, name="all-purpose cleaner spray", price=3.99, stock=95),
    Product(id=92, name="kitchen sponges (3 pack)", price=2.99, stock=125),
    # Personal Care
    Product(id=93, name="bar soap (4 pack)", price=5.49, stock=88),
    Product(id=94, name="volumizing shampoo (12 oz)", price=6.99, stock=72),
    Product(id=95, name="hydrating conditioner (12 oz)", price=6.99, stock=68),
    Product(id=96, name="fluoride toothpaste (6 oz)", price=3.79, stock=150),
    Product(id=97, name="deodorant stick", price=4.99, stock=110),
    Product(id=98, name="hand sanitizer (8 oz)", price=3.29, stock=200),
    Product(id=99, name="ibuprofen (100 ct)", price=8.99, stock=75),
    Product(id=100, name="adhesive bandages (60 ct)", price=4.49, stock=130),
]


@router.get("", response_model=List[Product])
def get_products(limit: int = None):
    if limit:
        return fake_products_db[:limit]
    return fake_products_db

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in fake_products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@router.post('', response_model=Product, status_code=201)
def create_product(product: ProductCreate):
    new_product_id = max(product.id for product in fake_products_db) + 1

    new_product = Product(
        id=new_product_id,
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    fake_products_db.append(new_product)
    return new_product


@router.patch('/{product_id}', response_model=Product)
def update_product(product_id: int, updated_product: ProductUpdate):
    for product in fake_products_db:
        if product.id == product_id:
            if updated_product.name is not None:
                product.name = updated_product.name

            if updated_product.price is not None:
                product.price = updated_product.price

            if updated_product.stock is not None:
                product.stock = updated_product.stock
            return product
    raise HTTPException(status_code=404,detail="Product not found")


@router.delete('/{product_id}', response_model=Product)
def delete_product(product_id: int):
    for index, product in enumerate(fake_products_db):
        if product.id == product_id:
            deleted_product = fake_products_db.pop(index)
            return deleted_product
    raise HTTPException(status_code=404,detail="Product not found")