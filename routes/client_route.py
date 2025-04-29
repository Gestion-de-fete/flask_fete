from flask import Blueprint, request, jsonify
from models.client_model import db, Client

client_bp = Blueprint('client', __name__, url_prefix='/clients')

@client_bp.route('/', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{
        'cin': c.cin_client,
        'nom': c.nom_client,
        'prenom': c.prenom_client,
        'email': c.email_client,
        'adresse': c.adresse_client,
        'telephone': c.telephone_client,
        'paf': c.paf_client,
        'codeqr': c.codeqr_client
    } for c in clients])

@client_bp.route('/', methods=['POST'])
def create_client():
    data = request.get_json()
    nouveau_client = Client(
        cin_client=data['cin_client'],
        id_utilisateur=data['id_utilisateur'],
        nom_client=data['nom_client'],
        prenom_client=data['prenom_client'],
        email_client=data['email_client'],
        adresse_client=data['adresse_client'],
        telephone_client=data['telephone_client'],
        paf_client=data['paf_client'],
        codeqr_client=data['codeqr_client']
    )
    db.session.add(nouveau_client)
    db.session.commit()
    return jsonify({"message": "Client créé avec succès."}), 201
