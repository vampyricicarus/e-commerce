from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:your_password@localhost/fitness_center_db'
db = SQLAlchemy(app)

class Customer:
    __tableone__ = "Customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, 255)
    password = db.Column(db.String, 255)
    email = db.Column(db.String, 255)
    phone = db.Column(db.Integer, 10)

class Product:
    __tabletwo__ = "Product"
    id = db.Column(db.Integer, foreign_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

@app.route("/customers", methods["POST"])
def post_customer():
    new_customer = Customer(name=name, password=password, email=email, phone=phone)
    db.session.add(new_customer)  
    db.session.commit()
    return new_customer

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    return Customer.query.get(id)

@app.route("/customers/update", methods=["PUT"])
def update_member(id, name, password, email, phone):
    customer = get_customer(id)
    if customer:
        if name is not None:
            customer.name = name
        if password is not None:
            customer.password = password
        if email is not None:
            customer.email = email
        if phone is not None:
            customer.phone = phone
        db.session.commit()
    return customer

@app.route("/customers/delete", methods=["DELETE"])
def delete_member(id):
    customer = get_customer(id)
    if customer:
        db.session.delete(customer)
        db.session.commit()

@app.route("/products", methods=["GET"])
def get_products(id):
    return Product.query.get(id)

@app.route("/products/update", methods=["PUT"])
def update_product(id, name, price):
    product = get_products(id)
    if product:
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        db.session.commit()
    return product

@app.route("/products/create", methods=["POST"])
def create_product():
    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()
    return new_product

@app.route("/products/delete", methods=["DELETE"])
def delete_product(id):
    product = get_products(id)
    if product:
        db.session.delete(product)
        db.session.commit()

app = Flask(__name__)

orders = {}
order_counter = 1

@app.route('/order', methods=['POST'])
def place_order():
    global order_counter
    data = request.json

    if not data or 'products' not in data or 'customer' not in data:
        return jsonify({'error': 'Invalid order data'}), 400

    order_id = order_counter
    order_counter += 1
    order_date = datetime.now().isoformat()

    order = {
        'id': order_id,
        'customer': data['customer'],
        'products': data['products'],
        'order_date': order_date,
        'status': 'Placed'  
    }

    orders[order_id] = order

    return jsonify(order), 201

@app.route('/order/<int:order_id>', methods=['GET'])
def retrieve_order(order_id):
    order = orders.get(order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify(order)

@app.route('/order/<int:order_id>/track', methods=['GET'])
def track_order(order_id):
    order = orders.get(order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    tracking_info = {
        'order_id': order['id'],
        'status': order['status'],
        'order_date': order['order_date'],
        'expected_delivery': "2023-10-25"  
    }

    return jsonify(tracking_info)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
