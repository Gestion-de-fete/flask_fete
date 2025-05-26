from flask import request, jsonify
from models.client_model import db, Client
from datetime import datetime

def filtrer_clients_par_date():
    try:
        # Récupérer les paramètres de requête (GET ?start=...&end=...)
        start_date_str = request.args.get('start')
        end_date_str = request.args.get('end')

        # Vérifier que les deux dates sont présentes
        if not start_date_str or not end_date_str:
            return jsonify({'error': 'Les paramètres start et end sont requis'}), 400

        # Convertir les dates en objets datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # Ajouter 1 jour à la date de fin pour inclure toute la journée
        end_date = end_date.replace(hour=23, minute=59, second=59)

        # Requête pour filtrer les clients entre les deux dates
        clients = Client.query.filter(
            Client.date_creation >= start_date,
            Client.date_creation <= end_date
        ).all()

        # Retourner les résultats en JSON
        resultats = []
        for client in clients:
            resultats.append({
                'cin_client': client.cin_client,
                'nom_client': client.nom_client,
                'prenom_client': client.prenom_client,
                'email_client': client.email_client,
                'paf_client' : client.paf_client,
                'date_creation': client.date_creation.strftime('%Y-%m-%d %H:%M:%S')
                
            })

        return jsonify(resultats), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
