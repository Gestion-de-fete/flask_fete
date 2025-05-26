from flask import jsonify
from models.entree_sortie_model import EntreeSortie

def get_entree_sortie():
    print(">>> get_entree_sortie appelée")
    try:
        entree_sorties = EntreeSortie.query.all()
        result = [
            {
                "id_entree_sortie": e.id_entree_sortie,
                "cin_client": e.cin_client,
                "nom": e.client.nom_client,       # correction ici
                "prenom": e.client.prenom_client, # correction ici
                "etat": e.etat,
                "date_heure": e.date_heure.strftime("%Y-%m-%d %H:%M:%S")
            }
            for e in entree_sorties
        ]
        return jsonify(result)
    except Exception as ex:
        print(f">>> Erreur : {ex}")
        return jsonify({"error": str(ex)}), 500
