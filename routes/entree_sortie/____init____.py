from flask import Blueprint
from .create_entree import demarrer_fete
from .update_entree import update_entree
from .update_sortie import update_sortie

# Création du blueprint avec un préfixe d'URL
entree_sortie_bp = Blueprint('entree_sortie', __name__, url_prefix='/api/entree_sortie')

# Définition des routes avec leurs méthodes HTTP
entree_sortie_bp.route('/create', methods=['POST'])(demarrer_fete)
entree_sortie_bp.route('/entree', methods=['PUT'])(update_entree)
entree_sortie_bp.route('/sortie', methods=['PUT'])(update_sortie)
