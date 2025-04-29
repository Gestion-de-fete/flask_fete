from flask import Blueprint
from .get_utilisateur import get_utilisateurs
from .create_utilisateur import create_utilisateur
from .valider_utilisateur import valider_utilisateur
from .login_utilisateur import login_utilisateur
from .logout_utilisateur import logout_utilisateur

utilisateur_bp = Blueprint('utilisateur', __name__, url_prefix='/api/utilisateur')

utilisateur_bp.route('/', methods=['GET'])(get_utilisateurs)
utilisateur_bp.route('/', methods=['POST'])(create_utilisateur)
utilisateur_bp.route('/validation/<int:id_utilisateur>', methods=['PUT'])(valider_utilisateur)
utilisateur_bp.route('/login', methods=['POST'])(login_utilisateur)
utilisateur_bp.route('/logout', methods=['POST'])(logout_utilisateur)
