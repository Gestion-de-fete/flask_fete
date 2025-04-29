from flask import request, jsonify
from models.utilisateur_model import db, Utilisateur
from routes.utilisateurs.emails import envoyer_email_utilisateur

def valider_utilisateur(id_utilisateur):
    data = request.get_json()
    statut = data.get('statut')

    print(f"Received statut: '{statut}'")  # Debug: Log the received statut value

    # Autoriser 'en attente', 'accepté', et 'refusé'
    if statut not in ['En attente', 'Accepté', 'Refusé']:
        print(f"Invalid statut: '{statut}'")  # Debug: Log invalid statut
        return jsonify({'message': 'Statut invalide. Utilisez "En attente", "Accepté" ou "Refusé".'}), 400

    utilisateur = Utilisateur.query.get(id_utilisateur)

    if not utilisateur:
        print(f"Utilisateur non trouvé: ID {id_utilisateur}")  # Debug: Log missing user
        return jsonify({'message': 'Utilisateur non trouvé.'}), 404

    if statut == 'Refusé':
        print(f"Deleting utilisateur: ID {id_utilisateur}")  # Debug: Log deletion attempt
        try:
            db.session.delete(utilisateur)
            db.session.commit()
            print(f"Utilisateur supprimé: ID {id_utilisateur}")  # Debug: Log successful deletion
            # Envoyer un email à l'utilisateur
            envoyer_email_utilisateur(utilisateur, statut)
            return jsonify({'message': 'Utilisateur refusé et supprimé avec succès.'})
        except Exception as e:
            print(f"Error deleting utilisateur: {str(e)}")  # Debug: Log deletion error
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la suppression de l’utilisateur.'}), 500
    else:
        print(f"Updating statut to '{statut}' for utilisateur: ID {id_utilisateur}")  # Debug: Log status update
        utilisateur.statut_utilisateur = statut
        db.session.commit()
        # Envoyer un email à l'utilisateur
        envoyer_email_utilisateur(utilisateur, statut)
        return jsonify({'message': f'Utilisateur mis à jour avec le statut "{statut}" avec succès.'})
