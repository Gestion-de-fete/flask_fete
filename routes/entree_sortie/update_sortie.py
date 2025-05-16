from flask import request, jsonify
from models.entree_sortie_model import db, EntreeSortie
from models.utilisateur_model import Utilisateur  # Si ce modèle est séparé

def update_sortie():
    data = request.get_json()

    id_utilisateur = data.get("id_utilisateur")
    cin_client = data.get("cin_client")

    # Vérifier le rôle de l'utilisateur
    utilisateur = Utilisateur.query.get(id_utilisateur)
    if not utilisateur or utilisateur.role_utilisateur != "securite_sortie":
        return jsonify({"message": "Accès refusé. Rôle non autorisé."}), 403

    # Rechercher l'entrée existante
    entree = EntreeSortie.query.filter_by(cin_client=cin_client).first()
    if not entree:
        return jsonify({"message": "Client non trouvé dans la base d'entrée."}), 404

    if entree.etat == "sortie":
        return jsonify({"message": "Le client est déjà sorti. Action inutile."}), 400

    # Mettre à jour l'état à "sortie"
    entree.etat = "sortie"
    db.session.commit()

    return jsonify({"message": "Sortie enregistrée. À bientôt."}), 200
