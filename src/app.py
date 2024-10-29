from flask import Flask, jsonify, request
from flask_cors import CORS
from Models.Modelo import Usuario,Producto
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
frontend_url= os.getenv("FRONTEND_URL")
CORS(app, resources={r"/*": {"origins": frontend_url}})



@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        usuario = Usuario.get(Usuario.usuario == data['usuario'].lower())
        print(usuario)
        if usuario.check_password(data['password']):
            return jsonify({'message': 'Inicio de sesión exitoso', 'id_usuario': usuario.id}), 200
        else:
            return jsonify({'error': 'Contraseña incorrecta'}), 200
    except Usuario.DoesNotExist:
        return jsonify({'error': 'Usuario no encontrado'}), 200
    
@app.route('/registrar', methods=['POST'])
def registrarUsuario():
    data = request.json
    usuario_nombre = data['usuario'].lower()
    
    try:
        # Busca si el usuario ya existe
        usuario = Usuario.get(Usuario.usuario == usuario_nombre)
        return jsonify({'error': 'Nombre de usuario ya existe, elija otro'}), 200
    
    except Usuario.DoesNotExist:
        # Si el usuario no existe, procede a crearlo
        nuevoUsuario = Usuario(usuario=usuario_nombre, password='')
        nuevoUsuario.set_password(data['password'])  # Asegúrate de tener el método `set_password` definido
        nuevoUsuario.save()
        return jsonify({'message': 'Usuario registrado exitosamente!'}), 200
    
    except Exception as e:
        # Si ocurre otro tipo de excepción, regresa un error genérico y el detalle del error para debugging
        return jsonify({'error': 'Error inesperado', 'detalle': str(e)}), 500

    
@app.route('/productos/<int:id_user>', methods=['GET'])
def obtenerProductos(id_user):
    try:
        # Obtiene el producto por su ID
        productos = Producto.select().where(Producto.idUsuario == id_user)
        print(productos)
        productos_list = []
        for producto in productos:
            productos_list.append({
                'id': producto.idProducto,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'cantidad': producto.cantidad
            })
    
        return jsonify(productos_list), 200 
    except Producto.DoesNotExist:
        return jsonify({'error': 'No hay productos'}), 200

@app.route('/producto/<int:id>/<int:id_user>', methods=['GET'])
def obtenerProductoId(id, id_user):
    try:
        producto = Producto.get(
            (Producto.idProducto == id) & (Producto.idUsuario == id_user)
        )
        print(type(producto.idProducto))
        producto_dict = {
            'id': producto.idProducto,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': producto.cantidad,
        }
        print(producto_dict)
        return jsonify(producto_dict), 200
    except Producto.DoesNotExist:
        return jsonify({'error': 'No se encontró un producto'}), 200

    
@app.route('/crearproducto/<int:id_user>', methods=['POST'])
def crearproducto(id_user):
    try:
        data = request.json
        producto = Producto(
            nombre=data['nombre'],
            precio=data['precio'],
            cantidad=data['cantidad'],
            idUsuario= id_user
        )
        producto.save()
    
        return jsonify({'message': 'Producto Creado Correctamente'}), 200 
    except Producto.DoesNotExist:
        return jsonify({'error': 'Error al crear producto'}), 200
    

@app.route('/editarproducto/<int:id>/<int:id_user>', methods=['PUT'])
def editarProducto(id_user, id):
    try:
        data = request.json
        producto = Producto.get((Producto.idProducto == id) & (Producto.idUsuario == id_user))
        producto.nombre = data['nombre']
        producto.precio = data['precio']
        producto.cantidad = data['cantidad']
        producto.save()

        return jsonify({'message': 'Producto actualizado correctamente'}), 200 
    except Producto.DoesNotExist:
        return jsonify({'error': 'Producto no encontrado'}), 200

@app.route('/eliminarproducto/<int:id>/<int:id_user>', methods=['DELETE'])
def eliminarproducto(id_user,id):
    try:
        Producto.delete().where(
            (Producto.idProducto == id) & (Producto.idUsuario == id_user)
        ).execute()
    
        return jsonify({'message': 'Producto Eliminado Correctamente'}), 200 
    except Producto.DoesNotExist:
        return jsonify({'error': 'Error al eliminar producto'}), 200


if __name__ == '__main__':
    app.run(debug=True)
