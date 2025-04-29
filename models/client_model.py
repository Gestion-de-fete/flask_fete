from ._init_ import db

class Client(db.Model):
    cin_client = db.Column(db.String, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    photo_client = db.Column(db.LargeBinary, nullable=False)
    nom_client = db.Column(db.String(100))
    prenom_client = db.Column(db.String(100))
    email_client = db.Column(db.String(100), unique=True, nullable=False)
    adresse_client = db.Column(db.String(50))
    telephone_client = db.Column(db.String(50))
    paf_client = db.Column(db.Integer, nullable=False)
    codeqr_client = db.Column(db.String(255), unique=True, nullable=False)

    entrees_sorties = db.relationship('EntreeSortie', backref='client', lazy=True)
