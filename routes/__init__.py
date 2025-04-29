from .utilisateur_route import utilisateur_bp
from .client_route import client_bp
from .entree_sortie_route import entreesortie_bp

def create_routes(app):
    app.register_blueprint(utilisateur_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(entreesortie_bp)
