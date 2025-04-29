from ._init_ import db

class Utilisateur(db.Model):
    id_utilisateur = db.Column(db.Integer, primary_key=True)  # Auto-incrémenté automatiquement
    nom_utilisateur = db.Column(db.String(100), nullable=True)
    prenom_utilisateur = db.Column(db.String(100), nullable=True)
    email_utilisateur = db.Column(db.String(100), unique=True, nullable=False)
    role_utilisateur = db.Column(db.String(20), nullable=False)
    statut_utilisateur = db.Column(db.String(15), nullable=False)
    mot_de_passe_utilisateur = db.Column(db.String(255), nullable=False)

    clients = db.relationship('Client', backref='utilisateur', lazy=True)
