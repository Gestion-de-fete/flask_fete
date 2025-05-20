from flask import jsonify
from models.entree_sortie_model import EntreeSortie

def get_etat():
    try:
        dernier_entree_sortie = EntreeSortie.query.order_by(EntreeSortie.id_entree_sortie.desc()).first()

        if dernier_entree_sortie:
            result = {
                "id_entree_sortie": dernier_entree_sortie.id_entree_sortie,
                "cin_client": dernier_entree_sortie.cin_client,
                "etat": dernier_entree_sortie.etat,
                "date_heure": dernier_entree_sortie.date_heure.isoformat() if dernier_entree_sortie.date_heure else None
            }
            return jsonify(result), 200
        else:
            # Aucun enregistrement, mais on renvoie un message 200 (OK)
            return jsonify({"message": "Aucun enregistrement trouvé"}), 200

    except Exception as e:
        print("Erreur lors de la récupération de l'état :", e)
        return jsonify({"error": "Erreur interne du serveur"}), 500
