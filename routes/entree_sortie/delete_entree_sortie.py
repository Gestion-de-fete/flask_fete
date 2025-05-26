from flask import jsonify
from models.entree_sortie_model import db, EntreeSortie

def delete_entree_sortie(id_entree_sortie):
    try:
        entree_sortie = EntreeSortie.query.get(id_entree_sortie)
        if not entree_sortie:
            return jsonify({'error': f'Entrée/Sortie avec id {id_entree_sortie} non trouvée'}), 404
        
        db.session.delete(entree_sortie)
        db.session.commit()
        return jsonify({'message': f'Entrée/Sortie avec id {id_entree_sortie}  supprimé avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la suppression: {str(e)}'}), 500