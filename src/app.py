from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Estudiante, Asignatura, Calificacion
import os

# Crear la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_la_aplicacion'

# Configurar la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con la aplicación
db.init_app(app)

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

# Rutas para estudiantes
@app.route('/estudiantes')
def listar_estudiantes():
    estudiantes = Estudiante.query.all()
    return render_template('estudiantes.html', estudiantes=estudiantes)

@app.route('/estudiantes/nuevo', methods=['GET', 'POST'])
def nuevo_estudiante():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        
        nuevo_est = Estudiante(nombre=nombre, apellidos=apellidos, email=email)
        db.session.add(nuevo_est)
        try:
            db.session.commit()
            flash('Estudiante agregado correctamente', 'success')
            return redirect(url_for('listar_estudiantes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar estudiante: {str(e)}', 'danger')
    
    return render_template('form_estudiante.html')

@app.route('/estudiantes/editar/<int:id>', methods=['GET', 'POST'])
def editar_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    if request.method == 'POST':
        estudiante.nombre = request.form['nombre']
        estudiante.apellidos = request.form['apellidos']
        estudiante.email = request.form['email']
        
        try:
            db.session.commit()
            flash('Estudiante actualizado correctamente', 'success')
            return redirect(url_for('listar_estudiantes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar estudiante: {str(e)}', 'danger')
    
    return render_template('form_estudiante.html', estudiante=estudiante)

@app.route('/estudiantes/eliminar/<int:id>')
def eliminar_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    try:
        db.session.delete(estudiante)
        db.session.commit()
        flash('Estudiante eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar estudiante: {str(e)}', 'danger')
    
    return redirect(url_for('listar_estudiantes'))

@app.route('/estudiantes/<int:id>/calificaciones')
def ver_calificaciones_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    calificaciones = Calificacion.query.filter_by(estudiante_id=id).all()
    return render_template('calificaciones_estudiante.html', estudiante=estudiante, calificaciones=calificaciones)

# Rutas para calificaciones
@app.route('/calificaciones/nueva', methods=['GET', 'POST'])
def nueva_calificacion():
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        asignatura_id = request.form['asignatura_id']
        nota = request.form['nota']
        
        nueva_cal = Calificacion(
            estudiante_id=estudiante_id,
            asignatura_id=asignatura_id,
            nota=float(nota)
        )
        
        db.session.add(nueva_cal)
        try:
            db.session.commit()
            flash('Calificación agregada correctamente', 'success')
            return redirect(url_for('listar_calificaciones'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar calificación: {str(e)}', 'danger')
    
    estudiantes = Estudiante.query.all()
    asignaturas = Asignatura.query.all()
    return render_template('form_calificacion.html', estudiantes=estudiantes, asignaturas=asignaturas)

@app.route('/calificaciones')
def listar_calificaciones():
    calificaciones = Calificacion.query.all()
    return render_template('calificaciones.html', calificaciones=calificaciones)

@app.route('/calificaciones/editar/<int:id>', methods=['GET', 'POST'])
def editar_calificacion(id):
    calificacion = Calificacion.query.get_or_404(id)
    if request.method == 'POST':
        calificacion.estudiante_id = request.form['estudiante_id']
        calificacion.asignatura_id = request.form['asignatura_id']
        calificacion.nota = float(request.form['nota'])
        
        try:
            db.session.commit()
            flash('Calificación actualizada correctamente', 'success')
            return redirect(url_for('listar_calificaciones'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar calificación: {str(e)}', 'danger')
    
    estudiantes = Estudiante.query.all()
    asignaturas = Asignatura.query.all()
    return render_template('form_calificacion.html', calificacion=calificacion, estudiantes=estudiantes, asignaturas=asignaturas)

@app.route('/calificaciones/eliminar/<int:id>')
def eliminar_calificacion(id):
    calificacion = Calificacion.query.get_or_404(id)
    try:
        db.session.delete(calificacion)
        db.session.commit()
        flash('Calificación eliminada correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar calificación: {str(e)}', 'danger')
    
    return redirect(url_for('listar_calificaciones'))

# Crear las tablas de la base de datos
with app.app_context():
    db.create_all()
    
    # Verificar si hay asignaturas, si no, crear algunas por defecto
    if not Asignatura.query.first():
        asignaturas_default = [
            Asignatura(nombre='Matemáticas', descripcion='Álgebra y cálculo'),
            Asignatura(nombre='Física', descripcion='Física general'),
            Asignatura(nombre='Química', descripcion='Química orgánica e inorgánica'),
            Asignatura(nombre='Programación', descripcion='Fundamentos de programación')
        ]
        db.session.add_all(asignaturas_default)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)