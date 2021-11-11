from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= 'mysql+pymysql://root@localhost/ventas'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
ma=Marshmallow(app)

class cliente(db.Model): ################################### Object db. Database structure
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String)
    apellido1=db.Column(db.String)
    apellido2=db.Column(db.String)
    ciudad=db.Column(db.String)
    categoria=db.Column(db.Integer)
    
    def __init__(self, nombre, apellido1, apellido2,ciudad,categoria):
        self.nombre=nombre
        self.apellido1=apellido1
        self.apellido2=apellido2
        self.ciudad=ciudad
        self.categoria=categoria
db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido1','apellido2','ciudad','categoria')

tasks_schema=TaskSchema(many=True)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/del',methods=['GET','POST'])
def delete():
    return render_template('del.html')

@app.route('/find',methods=['GET','POST'])
def consult():
    
    return render_template('find.html') 

@app.route('/consult',methods=['GET','POST'])
def consulta():
    all_clients=cliente.query.all()
    result=tasks_schema.dump(all_clients)
    clients=list(result)
#    clients=json.dumps(result)
    if request.method=='POST':
        consult=request.form['nombre']
        if consult !="":
            for i in clients:
                if consult==i['nombre']:
                    client={
                        'nombre':i['nombre'],
                        'apellido1':i['apellido1'],
                        'apellido2':i['apellido2'],
                        'ciudad':i['ciudad']
                    }
                    print(client)
                    return render_template('consult.html',**client)
    return 'cliente inexistente'

@app.route('/add',methods=['GET','POST'])
def add():
    return render_template('add.html')

@app.route('/addfinal',methods=['POST'])
def addfinal():
    if request.method=='POST':
        nombre=request.form['nombre']
        apellido1=request.form['apellido1']
        apellido2=request.form['apellido2']
        ciudad=request.form['ciudad']
        categoria=request.form['categoria']

        new_client=cliente(nombre,apellido1,apellido2,ciudad,categoria)
        db.session.add(new_client)
        db.session.commit()

        context={
            'nombre':nombre,
            'apellido1':apellido1,
            'apellido2':apellido2,
            'ciudad':ciudad,
            'categoria':categoria
        }
    return render_template('addfinal.html',**context)
    
if __name__=='__main__':
    app.run(debug=True)