from flask import Blueprint
from .update_entree import update_entree
from .update_sortie import update_sortie
from .get_etat import get_etat
from .get_entree_sortie import get_entree_sortie
from .dashboard import get_dashboard_data
from .delete_entree_sortie import delete_entree_sortie

# Création du blueprint avec un préfixe d'URL
entree_sortie_bp = Blueprint('entree_sortie', __name__, url_prefix='/api/entree_sortie')

# Définition des routes avec leurs méthodes HTTP
entree_sortie_bp.route('/entree', methods=['PUT'])(update_entree)
entree_sortie_bp.route('/sortie', methods=['PUT'])(update_sortie)
entree_sortie_bp.route('/etat', methods=['GET'])(get_etat)
entree_sortie_bp.route('/fetch', methods=['GET'])(get_entree_sortie)
entree_sortie_bp.route('/number', methods=['GET'])(get_dashboard_data)
entree_sortie_bp.route('/delete', methods=['DELETE'])(delete_entree_sortie)



