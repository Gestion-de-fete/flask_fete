from flask import Blueprint, request, jsonify
from models.entree_sortie_model import db, EntreeSortie

entreesortie_bp = Blueprint('entreesortie', __name__, url_prefix='/entreesortie')

@entreesortie_bp.route('/', methods=['POST'])
def create_entree_sortie():
    data = request.get_json()
    mouvement = EntreeSortie(
        cin_client=data['cin_client'],
        etat=data['etat']
    )
    db.session.add(mouvement)
    db.session.commit()
    return jsonify({"message": "Mouvement enregistré avec succès."}), 201
