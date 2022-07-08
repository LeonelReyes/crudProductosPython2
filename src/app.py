from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)
CORS(app)


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskmysqlonline:Mkomkomko@db4free.net/flaskmysqlonline'







# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskmysqlonline:Mkomkomko@db4free.net/flaskmysqlonline'



#                                               user:clave@localhost/nombreBaseDatos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
# defino la tabla


class Producto(db.Model):   # la clase Producto hereda de db.Model
    # define los campos de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)

    def __init__(self, nombre, precio, stock):  # crea el  constructor de la clase
        # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.nombre = nombre
        self.precio = precio
        self.stock = stock


db.create_all()  # crea las tablas
#  ************************************************************


class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'precio', 'stock')


producto_schema = ProductoSchema()            # para crear un producto
productos_schema = ProductoSchema(many=True)  # multiples registros


# crea los endpoint o rutas (json)
@app.route('/productos', methods=['GET'])
def get_Productos():
    all_productos = Producto.query.all()     # query.all() lo hereda de db.Model
    # .dump() lo hereda de ma.schema
    result = productos_schema.dump(all_productos)
    return jsonify(result)


@app.route('/productos/<id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    return producto_schema.jsonify(producto)


@app.route('/producto/<id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)


@app.route('/productos', methods=['POST'])  # crea ruta o endpoint
def create_producto():
    print(request.json)  # request.json contiene el json que envio el cliente
    nombre = request.json['nombre']
    precio = request.json['precio']
    stock = request.json['stock']
    new_producto = Producto(nombre, precio, stock)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)


@app.route('/productos/<id>', methods=['PUT'])
def update_producto(id):
    producto = Producto.query.get(id)
    nombre = request.json['nombre']
    precio = request.json['precio']
    stock = request.json['stock']

    producto.nombre = nombre
    producto.precio = precio
    producto.stock = stock
    db.session.commit()
    return producto_schema.jsonify(producto)


# programa principal *******************************
if __name__ == '__main__':
    app.run(debug=True, port=5000)
