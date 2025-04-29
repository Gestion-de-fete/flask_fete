from flask import jsonify
from models.utilisateur_model import Utilisateur

def get_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return jsonify([
        {
            'id': u.id_utilisateur,
            'nom': u.nom_utilisateur,
            'prenom': u.prenom_utilisateur,
            'email': u.email_utilisateur,
            'role': u.role_utilisateur,
            'statut': u.statut_utilisateur
        }
        for u in utilisateurs
    ])
