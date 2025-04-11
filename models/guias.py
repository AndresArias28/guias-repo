from mongoengine import *
from models.instructores import Instructores

class Guias(Document):
    nombre = StringField(required=True)
    descripcion = StringField(required=True)
    programa = StringField(required=True)
    documento_pdf = StringField(required=True)
    fecha = DateTimeField(required=True)
    instructor =  ReferenceField(Instructores, reverse_delete_rule=DENY, required=True)
    
    def __str__(self):
        return self.nombre
    