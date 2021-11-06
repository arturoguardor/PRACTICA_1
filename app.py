from re import split
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime as date


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Red5g123@localhost:3306/db_restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

today = date.now().strftime('%d/%m/%Y %H:%M:%S')

class Products_Table(db.Model):

    product_id = db.Column(db.Integer,primary_key=True)
    products_name = db.Column(db.String(100))
    product_price = db.Column(db.Integer)

    #Constructor cada vez que se instancia la clase
    #Al recibir asignar los datos
    def __init__(self, products_name, product_price):

        self.products_name= products_name
        self.product_price= product_price
    #Modelo de Datos completado

class Orders_Table(db.Model):

    order_id = db.Column(db.Integer,primary_key=True)
    client_name = db.Column(db.String(100))
    order_date = db.Column(db.DateTime(100))
    products_name = db.Column(db.String(100))
    no_product = db.Column(db.Integer)
    total_count = db.Column(db.Integer)
    client_addrs = db.Column(db.String(100))
    client_city = db.Column(db.String(100))
    client_phone = db.Column(db.String(100))
    status_order = db.Column(db.String(100), default="EN ESPERA")
    check_preparation = db.Column(db.String(100), default=today)
    check_on_route = db.Column(db.String(100))
    check_delivered = db.Column(db.String(100))

    #Constructor cada vez que se instancia la clase
    #Al recibir asignar los datos
    def __init__(
                 self, client_name, order_date, products_name,
                 no_product, total_count, client_addrs,
                 client_city, client_phone, status_order,
                 check_preparation, check_on_route, check_delivered):

        self.client_name = client_name
        self.order_date = order_date
        self.products_name = products_name
        self.no_product = no_product
        self.total_count = total_count
        self.client_addrs = client_addrs
        self.client_city = client_city
        self.client_phone = client_phone
        self.status_order = status_order
        self.check_preparation = check_preparation
        self.check_on_route = check_on_route
        self.check_delivered = check_delivered
    #Modelo de Datos completado


db.create_all()

class Products_Table_Schema(ma.Schema):
    class Meta:
        fields = ('product_id ','products_name','product_price')

class Orders_Table_Schema(ma.Schema):
    class Meta:
        fields = (
                  'order_id ', 'client_name', 'order_date',
                  'products_name', 'no_product', 'total_count',
                  'client_addrs', 'client_city', 'client_phone',
                  'status_order', 'check_preparation', 'check_on_route',
                  'check_delivered')

product_table_schema = Products_Table_Schema()
products_table_schema = Products_Table_Schema(many=True)

order_table_schema = Orders_Table_Schema()
orders_table_schema = Orders_Table_Schema(many=True)

@app.route("/findoneorder/<id>",methods=["GET"])
def get_categoria_x_id():
    try:
        one_order = Orders_Table.query.get(id)
        return orders_table_schema.jsonify({
                                    "code": 200,
                                    "data": one_order,
                                    "status": "ok",
                                    "message": "Orders Displayed",
                                    "time": today})
    except Exception:
        return jsonify({
                        "code": 500,
                        "data": {},
                        "status_order": "error",
                        "message": "Read Error",
                        "time": today
        })


#Leer todos las ordenes
@app.route('/findallorders', methods=['GET'])
def findallorders():
    try:
        allorders = Orders_Table_Schema.query.all()
        result = orders_table_schema.dump(allorders)

        return orders_table_schema.jsonify({
                                    "code": 200,
                                    "data": result,
                                    "status": "ok",
                                    "message": "Orders Displayed",
                                    "time": today})
    except Exception:
        return jsonify({
                        "code": 500,
                        "data": {},
                        "status_order": "error",
                        "message": "Read Error",
                        "time": today
        })

#Actualizar Estado del pedido
@app.route('/updateorder/<id>', methods=['PUT'])
def update_order(order_id):
    try:
        update_order = Orders_Table.query.get(order_id)

        data = request.get_json(force=True)
        status_order = data['status_order']
        status_order = status_order.uppecase()

        if status_order == "EN PREPARACIÓN":
            update_order.status_order = status_order
            update_order.check_preparation = today
        elif status_order == "EN REPARTO":
            update_order.status_order = status_order
            update_order.check_on_route = today
        elif status_order == "ENTREGADO":
            update_order.status_order = status_order
            update_order.check_delivered = today
        else:
            return jsonify({
                        "code": 400,
                        "data": {},
                        "status_order": "error",
                        "message": "Bad Request",
                        "time": today})

        return orders_table_schema.jsonify({
                                    "code": 200,
                                    "data": status_order,
                                    "status": "ok",
                                    "message": "Order Updated",
                                    "time": today})
    except Exception:
        return jsonify({
                        "code": 500,
                        "data": {},
                        "status_order": "error",
                        "message": "Update Error",
                        "time": today})

#Crear Pedido
@app.route("/createorder", methods=['POST'])
def insert_order():
    try:
        data = request.get_json(force=True)
        client_name = data['client_name']
        products_name = data['products_name']
        client_addrs = data['client_addrs']
        client_city = data['client_city']
        client_phone = data['client_phone']

        order_date = today
        total_count = 0

        if products_name.count(",") >= 1:
            products_name = products_name.split(",")
            no_product = len(products_name)
            for product in products_name:
                products_name = product.strip()
                product = Products_Table.query.get(products_name)
                if product:
                    total_count += int(product['product_price'])
        else:
            product = Products_Table.query.get(products_name)
            total_count = int(product['product_price'])

        new_order = Orders_Table(
                                 client_name, order_date, products_name, 
                                 no_product, total_count, client_addrs,
                                 client_city, client_phone)

        db.session.add(new_order)
        db.session.commit()

        return jsonify({
                        "code": 200,
                        "data": new_order,
                        "status": "ok",
                        "message": "Order Created",
                        "time": today})
    except Exception:
        return jsonify({
                        "code": 500,
                        "data": {},
                        "status_order": "error",
                        "message": "Update Error",
                        "time": today})

#Crear articulo (Comida)
@app.route("/createfood", methods=['POST'])
def insert_food():
    try:
        data = request.get_json(force=True)
        products_name = data["products_name"]
        product_price = data["product_price"]

        new_food = Products_Table(products_name, product_price)
        db.session.add(new_food)
        db.session.commit()

        return jsonify({
                        "code": 200,
                        "data": new_food,
                        "status": "ok",
                        "message": "Food Created",
                        "time": today})
    except Exception:
        return jsonify({
                        "code": 500,
                        "data": {},
                        "status_order": "error",
                        "message": "Update Error",
                        "time": today})

@app.route('/', methods=['GET'])
def home():
    return jsonify({
                    'Message': 'Products CRUD',
                    'For Create New Product': '/createfood',
                    'For Create Order': '/createorder',
                    'For Read All Orders': '/findallorders',
                    'For Update Order': '/updateorder'})


if __name__ == '__main__':
    app.run(port=5000, debug=True)