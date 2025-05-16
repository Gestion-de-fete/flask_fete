from flask import request, jsonify
from models.entree_sortie_model import db, EntreeSortie
from models.utilisateur_model import Utilisateur  # Import modèle utilisateur
from datetime import datetime
from sqlalchemy import and_

def demarrer_fete():
    data = request.get_json()
    cin = data.get('cin_client')
    id_user = data.get('id_utilisateur')

    utilisateur = Utilisateur.query.get(id_user)
    if not utilisateur or utilisateur.role_utilisateur not in ["admin", "securite_entree"]:
        return jsonify({"message": "Accès refusé. Seuls les admins ou la sécurité d'entrée peuvent enregistrer un nouveau client."}), 403

    # Vérifie si ce client est déjà enregistré pour cette fête par cet utilisateur
    existing = EntreeSortie.query.filter(
        and_(
            EntreeSortie.cin_client == cin,
            EntreeSortie.id_utilisateur == id_user
        )
    ).first()

    if existing:
        return jsonify({"message": "Client déjà enregistré."}), 200

    nouvel_entree = EntreeSortie(
        cin_client=cin,
        id_utilisateur=id_user,
        etat="entree",  # par défaut lors de l’enregistrement initial
        date_heure=datetime.utcnow()
    )

    db.session.add(nouvel_entree)
    db.session.commit()

    return jsonify({"message": "Client ajouté et autorisé à entrer dans la fête."}), 201
