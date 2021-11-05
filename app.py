from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy, ForeignKey
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Red5gMySQL_8@localhost:3306/db_restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

class products_table(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(100))
    product_price = db.Column(db.Integer)

    #Constructor cada vez que se instancia la clase
    #Al recibir asignar los datos
    def __init__(self, product_name, product_price):
        self.product_name= product_name
        self.product_price= product_price
    #Modelo de Datos completado

class orders_table(db.Model):
    order_id = db.Column(db.Integer,primary_key=True)
    client_name = db.Column(db.String(100))
    order_date = db.Column(db.DateTime(100))
    no_product = db.Column(db.Integer)
    total_count = db.Column(db.Integer)
    client_addrs = db.Column(db.String(100))
    client_city = db.Column(db.String(100))
    client_phone = db.Column(db.String(100))
    status_order = db.Column(db.String(100), default="EN ESPERA")
    product_id = db.Column(db.Integer, ForeignKey("products_table.product_id"))

    #Constructor cada vez que se instancia la clase
    #Al recibir asignar los datos
    def __init__(
                 self, client_name, order_date, 
                 no_product, total_count, 
                 client_addrs, client_city, 
                 client_phone, status_order,
                 product_id):
        self.client_name = client_name
        self.order_date = order_date
        self.no_product = no_product
        self.total_count = total_count
        self.client_addrs = client_addrs
        self.client_city = client_city
        self.client_phone = client_phone
        self.status_order = status_order
        self.product_id = product_id
    #Modelo de Datos completado

db.create_all()

class Products_Table_Schema(ma.Schema):
    class Meta:
        fields = ('product_id ','product_name','product_price')

class Orders_Table_Schema(ma.Schema):
    class Meta:
        fields = (
                  'product_id ', 'client_name', 'order_date',
                  'no_product', 'total_count', 'client_addrs'
                  'client_city', 'client_phone', 'status_order',
                  'product_id')

products_table = Products_Table_Schema()
products_table = Products_Table_Schema(many=True)

orders_table = Orders_Table_Schema()
orders_table = Orders_Table_Schema(many=True)

