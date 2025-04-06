from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mini_projet.sqlite3'
app.config['SECRET_KEY'] = 'Zeiny-code hello ??'
db = SQLAlchemy(app)

# Création des modèles de données
class Intervenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    poste = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nom, prenom, poste):
        self.nom = nom
        self.prenom = prenom
        self.poste = poste

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    direction = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nom, prenom, direction):
        self.nom = nom
        self.prenom = prenom
        self.direction = direction

class Intervention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    motive = db.Column(db.String(255), nullable=False)
    etat = db.Column(db.String(10), nullable=False)
    intervenant_id = db.Column(db.Integer, db.ForeignKey('intervenant.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    
    def __init__(self, date, type, motive, etat, intervenant_id, client_id):
        self.date = date
        self.type = type
        self.motive = motive
        self.etat = etat
        self.intervenant_id = intervenant_id
        self.client_id = client_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and password == user.password:
        session['auth'] = True
        return redirect(url_for('homme'))
    else:
        return redirect(url_for('index'))
    
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html', error='Username already exists. Please choose another.')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['auth'] = True
        return redirect(url_for('homme'))
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
@app.route('/homme')
def homme():
    if session :
        return render_template('homme.html')
    else :
        return redirect(url_for('index'))
@app.route('/clients')
def clients():
    if session :
        clients = Client.query.all()
        return render_template('Clients.html', clients=clients)
    else :
        return redirect(url_for('index'))

@app.route('/Intervenant')
def intervenant():
    if session :
        Intervenants = Intervenant.query.all()
        return render_template('Intervenant.html', Intervenants=Intervenants)
    else :
        return redirect(url_for('index'))

@app.route('/Intervention')
def intervention():
    if session['auth'] :
        Interventions = Intervention.query.all()
        a, b = graphe()
        return render_template('Intervention.html', Interventions = Interventions, a = a, b = b)
    else :
        return redirect(url_for('index'))

@app.route('/clients_form')
def clients_form():
    return render_template('client_form.html')

@app.route('/Intervenant_form')
def intervenant_form():
    return render_template('intervenant_form.html')

@app.route('/add_intervention')
def intervention_form():
    clients = Client.query.all()
    intervenants = Intervenant.query.all()
    return render_template('intervention_form.html', clients=clients, intervenants=intervenants)

@app.route('/add_intervenant', methods=['POST'])
def add_intervenant():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        poste = request.form.get('poste')
        new_intervenant = Intervenant(nom=nom, prenom=prenom, poste=poste)
        db.session.add(new_intervenant)
        db.session.commit()
    return redirect(url_for('intervenant'))

@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        direction = request.form.get('direction')
        new_client = Client(nom=nom, prenom=prenom, direction=direction)
        db.session.add(new_client)
        db.session.commit()
    return redirect(url_for('clients'))

@app.route('/add_intervention', methods=['POST'])
def add_intervention():
    if request.method == 'POST':
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d')
        intervention_type = request.form.get('type')
        motive = request.form.get('motive')
        etat = request.form.get('etat')
        intervenant_id = request.form.get('intervenant_id')
        client_id = request.form.get('client_id')
        new_intervention = Intervention(
            date=date,
            type=intervention_type,
            motive=motive,
            etat=etat,
            intervenant_id=intervenant_id,
            client_id=client_id
        )
        db.session.add(new_intervention)
        db.session.commit()
    return redirect(url_for('intervention'))

@app.route('/delete_intervenant/<int:intervenant_id>', methods=['GET', 'POST'])
def delete_intervenant(intervenant_id):
    intervenant = Intervenant.query.filter_by(id=intervenant_id).first()
    db.session.delete(intervenant)
    db.session.commit()
    return redirect(url_for('intervenant'))

@app.route('/delete_client/<int:client_id>', methods=['GET', 'POST'])
def delete_client(client_id):
    client = Client.query.filter_by(id=client_id).first()
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients'))

@app.route('/delete_intervention/<int:intervention_id>', methods=['GET', 'POST'])
def delete_intervention(intervention_id):
    intervention = Intervention.query.filter_by(id=intervention_id).first()
    db.session.delete(intervention)
    db.session.commit()
    return redirect(url_for('intervention'))

@app.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        client.nom = request.form['nom']
        client.prenom = request.form['prenom']
        client.direction = request.form['direction']
        db.session.commit()
        return redirect(url_for('clients'))
    return render_template('edit_client.html', client=client)

@app.route('/edit_intervenant/<int:intervenant_id>', methods=['GET', 'POST'])
def edit_intervenant(intervenant_id):
    intervenant = Intervenant.query.get_or_404(intervenant_id)
    if request.method == 'POST':
        intervenant.nom = request.form['nom']
        intervenant.prenom = request.form['prenom']
        intervenant.poste = request.form['poste']
        db.session.commit()
        return redirect(url_for('intervenant'))
    return render_template('edit_intervenant.html', intervenant=intervenant)

@app.route('/edit_intervention/<int:intervention_id>', methods=['GET', 'POST'])
def edit_intervention(intervention_id):
    intervention = Intervention.query.filter_by(id=intervention_id).first()
    if request.method == 'POST':
        date_str = request.form['date']
        intervention.date = datetime.strptime(date_str, '%Y-%m-%d')
        intervention.type = request.form['type']
        intervention.motive = request.form['motive']
        intervention.etat = request.form['etat']
        intervention.intervenant_id = request.form['intervenant_id']
        intervention.client_id = request.form['client_id']
        db.session.commit()
        return redirect(url_for('intervention'))
    clients = Client.query.all()
    intervenants = Intervenant.query.all()
    return render_template('edit_intervention.html', intervention = intervention, clients = clients, intervenants = intervenants)
def graphe():
    total_realisee = Intervention.query.filter_by(etat="réalisée").count()
    if total_realisee == 0:
        labels = []
        values = []
    else:
        int = Intervenant.query.all()
        labels = []
        values = []
        for intervenant in int:
            total_int = 0
            interventions = Intervention.query.filter_by(etat="réalisée", intervenant_id=intervenant.id)
            for intervention in interventions:
                total_int += 1
            labels.append(intervenant.nom)
            values.append((total_int / total_realisee) * 100)
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    graph_html = pio.to_html(fig, full_html=False)
    count_realisee = Intervention.query.filter_by(etat="réalisée").count()
    count_en_attente = Intervention.query.filter_by(etat="en attente").count()
    fig2 = go.Figure(data=[go.Pie(labels=["réalisée", "en attente"], values=[count_realisee, count_en_attente])])
    graph_html2 = pio.to_html(fig2, full_html=False)
    return graph_html, graph_html2

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000,debug=True)
