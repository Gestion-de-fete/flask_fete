from flask import request, jsonify
from datetime import datetime
from models.entree_sortie_model import db, EntreeSortie
from models.utilisateur_model import Utilisateur
from models.client_model import Client  # Ajout import Client, nécessaire pour vérifier existence client

def demarrer_fete():
    data = request.get_json()

    cin_client = data.get('cin_client')
    id_user = data.get('id_utilisateur')
    etat = data.get('etat', 'entree')  # Par défaut "entree"

    # Validation des champs obligatoires
    if not cin_client:
        return jsonify({"error": "Le champ 'cin_client' est obligatoire."}), 400

    if not id_user:
        return jsonify({"error": "Le champ 'id_utilisateur' est obligatoire."}), 400

    # Vérification que le client existe bien
    client = Client.query.filter_by(cin_client=cin_client).first()
    if not client:
        return jsonify({"error": "Client non trouvé avec ce CIN."}), 404

    # Vérification que l'utilisateur a le bon rôle
    utilisateur = Utilisateur.query.get(id_user)
    if not utilisateur or utilisateur.role_utilisateur not in ["admin", "securite_entree"]:
        return jsonify({"error": "Accès refusé."}), 403

    # Vérification doublon (client déjà enregistré)
    existing = EntreeSortie.query.filter_by(cin_client=cin_client).first()
    if existing:
        return jsonify({"message": "Client déjà enregistré."}), 200

    # Création et insertion de la nouvelle entrée
    nouvel_entree = EntreeSortie(
        cin_client=cin_client,
        etat=etat,
        date_heure=datetime.utcnow()
    )

    try:
        db.session.add(nouvel_entree)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erreur lors de l'enregistrement", "details": str(e)}), 500

    return jsonify({"message": "Client ajouté et autorisé à entrer dans la fête."}), 201
