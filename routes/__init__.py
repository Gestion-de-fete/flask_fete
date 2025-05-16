from .utilisateurs._init_ import utilisateur_bp
from .client.___init___ import client_bp
from .entree_sortie.____init____ import entree_sortie_bp

def create_routes(app):
    app.register_blueprint(utilisateur_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(entree_sortie_bp)
