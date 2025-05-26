from flask import jsonify
from models.client_model import Client
from models.utilisateur_model import Utilisateur
from models.entree_sortie_model import EntreeSortie
from sqlalchemy import func
from datetime import datetime

def get_dashboard_data():
    # Nombre total de clients
    nombre_clients = Client.query.count()

    # Nombre total d’utilisateurs
    nombre_utilisateurs = Utilisateur.query.count()

    # Nombre total d’entrées et sorties
    nombre_entrees_sorties = EntreeSortie.query.count()

    # Histogramme des entrées par jour de la semaine (compatible PostgreSQL)
    histogramme_raw = (
        EntreeSortie.query
        .with_entities(func.extract('dow', EntreeSortie.date_heure).label('jour_semaine'), func.count().label('total'))
        .filter(EntreeSortie.etat == 'entree')
        .group_by('jour_semaine')
        .order_by('jour_semaine')  # Pour les afficher dans l’ordre
        .all()
    )

    jours_semaine = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam']
    histogramme = [
        {
            "jour": jours_semaine[int(float(row.jour_semaine))],  # conversion float → int
            "entrees": int(row.total)
        }
        for row in histogramme_raw
    ]

    return jsonify({
        "nombre_clients": nombre_clients,
        "nombre_utilisateurs": nombre_utilisateurs,
        "nombre_entrees_sorties": nombre_entrees_sorties,
        "histogramme": histogramme
    })
