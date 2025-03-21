from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializar la extensión SQLAlchemy
db = SQLAlchemy()

# Modelo para Estudiante
class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    calificaciones = db.relationship('Calificacion', backref='estudiante', lazy=True)

    def __repr__(self):
        return f'<Estudiante {self.nombre} {self.apellidos}>'

# Modelo para Asignatura
class Asignatura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    calificaciones = db.relationship('Calificacion', backref='asignatura', lazy=True)

    def __repr__(self):
        return f'<Asignatura {self.nombre}>'

# Modelo para Calificación
class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)
    asignatura_id = db.Column(db.Integer, db.ForeignKey('asignatura.id'), nullable=False)
    
    def __repr__(self):
        return f'<Calificacion {self.nota}>'