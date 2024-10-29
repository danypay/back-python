from peewee import *
import bcrypt

db = SqliteDatabase('.\data.db')

class BaseModel(Model):
    class Meta: 
        database = db

class Usuario(BaseModel):
    id = AutoField()
    usuario = CharField(unique=True)
    password = CharField()

    def set_password(self, password):
        # Hashear la contraseña y almacenar en el campo password
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # Verificar la contraseña
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Producto(BaseModel):
    idProducto = AutoField()
    nombre = CharField()
    precio = FloatField()
    cantidad = IntegerField()
    idUsuario = ForeignKeyField(Usuario, backref='productos')

# Conectar a la base de datos y crear tablas
if not db.is_closed():
    db.close()
db.connect()
db.create_tables([Usuario,Producto])




