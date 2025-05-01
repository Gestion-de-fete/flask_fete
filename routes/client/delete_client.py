from flask import jsonify
from models.client_model import db, Client

def delete_client(cin_client):
    try:
        client = Client.query.get(cin_client)
        if not client:
            return jsonify({'error': f'Client avec cin_client {cin_client} non trouvé'}), 404
        
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': f'Client avec cin_client {cin_client} supprimé avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la suppression du client: {str(e)}'}), 500