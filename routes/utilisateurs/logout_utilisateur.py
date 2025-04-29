from flask import jsonify, session

def logout_utilisateur():
    session.pop('utilisateur_id', None)
    session.pop('role', None)
    session.modified = True
    return jsonify({'message': 'Déconnexion réussie. La session a été terminée.'}), 200
