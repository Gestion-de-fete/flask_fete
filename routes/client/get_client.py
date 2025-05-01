from flask import jsonify
from models.client_model import Client
import base64

def get_client():
    try:
        clients = Client.query.all()
        if not clients:
            return jsonify({'message': 'Aucun client trouvé'}), 200
        
        return jsonify([
            {
                'id_client': c.cin_client,
                'id_utilisateur': c.id_utilisateur,
                'image': (base64.b64encode(c.photo_client).decode('utf-8') 
                         if isinstance(c.photo_client, bytes) 
                         else c.photo_client) if c.photo_client else None,
                'nom': c.nom_client,
                'prenom': c.prenom_client,
                'email': c.email_client,
                'adresse': c.adresse_client,
                'telephone': c.telephone_client,
                'paf': c.paf_client,
                'qr_code': (base64.b64encode(c.codeqr_client).decode('utf-8') 
                           if isinstance(c.codeqr_client, bytes) 
                           else c.codeqr_client) if c.codeqr_client else None
            }
            for c in clients
        ]), 200
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des clients: {str(e)}'}), 500