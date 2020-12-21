from flask import Flask,render_template,url_for,redirect,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
Bootstrap(app)


#Configuracion de conexion de postgresql
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://adminDB:1234@localhost:5432/escolares1'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://qrixyfqelpqzxa:d24aa68423a7faefb967db25772f9029c19318f281a575629e6cb449a8027dc1@ec2-3-220-23-212.compute-1.amazonaws.com:5432/d9techbmelo0kr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
#modelo de datos
class Alumnos(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(30)) 
    apellido = db.Column(db.String(30)) 
lista = ["Acerca","Nosotros","Contacto","Preguntas Frecuentes"]

@app.route("/",methods=['GET','POST'])
def index():
    print("index")
    if request.method == "POST":
        print("request")
        pnombre = request.form['nombre']
        papellido = request.form['apellido']
        alumno = Alumnos(nombre=pnombre,apellido=papellido)
        db.session.add(alumno)
        db.session.commit()
        mensaje = "Alumno registrado"
        return render_template("index.html",mensaje = mensaje)
    
    return render_template("index.html",variable=lista)
    #return redirect(url_for("acerca"))
@app.route("/acerca")
def acerca():
    consulta = Alumnos.query.all()
    print(consulta)
    return render_template("acerca.html",variable=consulta)
@app.route("/eliminar/<id>")
def eliminar(id):
    consulta = Alumnos.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for("acerca"))
@app.route("/editar/<id>")
def editar(id):
    consulta = Alumnos.query.filter_by(id=int(id)).first()
    db.session.commit()
    return render_template("editar.html",datos = consulta)
@app.route("/actualizar",methods=['GET','POST'])
def actualizar():
    if request.method == "POST":
        consulta = Alumnos.query.get(request.form['id'])
        consulta.nombre = request.form['nombre']
        consulta.apellido = request.form['apellido']
        db.session.commit()
        return redirect(url_for("acerca"))
if __name__ == "__main__":
    app.run(debug=True)