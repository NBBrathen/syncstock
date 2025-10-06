from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_products(db: Session, limit: int = None):
    query = db.query(models.Product)
    if limit:
        query = query.limit(limit)
    return query.all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if db_product is None:
        return None

    if product_update.name is not None:
        db_product.name = product_update.name
    if product_update.price is not None:
        db_product.price = product_update.price
    if product_update.stock is not None:
        db_product.stock = product_update.stock

    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if db_product is None:
        return None

    db.delete(db_product)
    db.commit()
    return db_product

# ORDERS

def get_orders(db: Session, limit: int = None):
    query = db.query(models.Order)
    if limit:
        query = query.limit(limit)
    return query.all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db: Session, order: schemas.OrderCreate):
    total_amount = 0.0 # Start off with no cost
    product_data = [] # Store the product data in a list

    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()

        if product is None:
            raise ValueError(f"Product with id {item.product_id} not found")

        if product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for product '{product.name}'. Available: {product.stock}, Requested: {item.quantity}")

        line_total = product.price * item.quantity
        total_amount += line_total

        product_data.append({
            'product': product,
            'quantity': item.quantity,
            'price': product.price
        })

    db_order = models.Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        customer_address=order.customer_address,
        total_amount=total_amount,
        status="pending"
    )

    db.add(db_order)
    db.flush()

    for data in product_data:
        order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=data['product'].id,
            quantity=data['quantity'],
            price_at_purchase=data['price']
        )
        db.add(order_item)

        data['product'].stock -= data['quantity']

    db.commit()
    db.refresh(db_order)

    return db_order

def update_order_status(db: Session, order_id: int, status: str):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if db_order is None:
        return None

    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

def cancel_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if db_order is None:
        return None

    if db_order.status == "delivered":
        raise ValueError("Cannot cancel a delivered order")

    # Get all order items to restore inventory
    order_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()

    # Restore inventory for each item
    for item in order_items:

        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if product:
            product.stock += item.quantity

    # Update order status to cancelled
    db_order.status = "cancelled"
    db.commit()
    db.refresh(db_order)
    return db_order


