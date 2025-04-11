from mongoengine import *

class Instructores(Document):
    nombre = StringField(required=True)
    email = StringField(required=True)
    regional = StringField(required=True)
    password = StringField(required=True)
    
    def __str__(self):
        return self.nombre
