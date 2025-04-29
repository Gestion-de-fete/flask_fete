from flask import request, jsonify
from werkzeug.security import generate_password_hash
from models.utilisateur_model import db, Utilisateur
from routes.utilisateurs.emails import envoyer_email_admin

def create_utilisateur():
    data = request.get_json()
    mot_de_passe_hache = generate_password_hash(data['mot_de_passe_utilisateur'])

    nouvel_utilisateur = Utilisateur(
        nom_utilisateur=data['nom_utilisateur'],
        prenom_utilisateur=data['prenom_utilisateur'],
        email_utilisateur=data['email_utilisateur'],
        role_utilisateur=data['role_utilisateur'],
        statut_utilisateur='En attente',
        mot_de_passe_utilisateur=mot_de_passe_hache
    )

    db.session.add(nouvel_utilisateur)
    db.session.commit()

    envoyer_email_admin(nouvel_utilisateur)

    return jsonify({"message": "Inscription soumise pour validation par l'administrateur."}), 201
