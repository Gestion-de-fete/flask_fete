from flask import request, jsonify, session
from werkzeug.security import check_password_hash
from models.utilisateur_model import Utilisateur

def login_utilisateur():
    data = request.get_json()
    email = data.get('email_utilisateur')
    mot_de_passe = data.get('mot_de_passe_utilisateur')

    utilisateur = Utilisateur.query.filter_by(email_utilisateur=email).first()

    if utilisateur and check_password_hash(utilisateur.mot_de_passe_utilisateur, mot_de_passe):
        if utilisateur.statut_utilisateur != 'accepté':
            return jsonify({'message': 'Votre inscription n\'a pas été acceptée.'}), 403
        
        session['utilisateur_id'] = utilisateur.id_utilisateur
        session['role'] = utilisateur.role_utilisateur

        return jsonify({
            'message': 'Connexion réussie.',
            'id_utilisateur': utilisateur.id_utilisateur,
            'role_utilisateur': utilisateur.role_utilisateur
        }), 200

    return jsonify({'message': 'Email ou mot de passe incorrect.'}), 401
