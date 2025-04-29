from ._init_ import db
from datetime import datetime

class EntreeSortie(db.Model):
    id_entree_sortie = db.Column(db.Integer, primary_key=True)
    cin_client = db.Column(db.String, db.ForeignKey('client.cin_client'), nullable=False)
    etat = db.Column(db.String(10), nullable=False)  # 'entree' ou 'sortie'
    date_heure = db.Column(db.DateTime, default=datetime.utcnow)
