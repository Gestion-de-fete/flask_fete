# import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/fete'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = 'z7j!5e^g2@9$pl%f@r3q&bxcv8*k(4n#dh@1$9u6s7h+w2ljvn'

#     MAIL_SERVER = 'smtp.gmail.com'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USE_SSL = False
#     MAIL_USERNAME = 'heritianajulien45@gmail.com'
#     MAIL_PASSWORD = 'bysg pzyd umap fvog'
#     MAIL_DEFAULT_SENDER = 'heritianajulien45@gmail.com'
import os

class Config:
    # Configuration de la base de données PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/fete'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactiver le suivi des modifications pour économiser de la mémoire
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'z7j!5e^g2@9$pl%f@r3q&bxcv8*k(4n#dh@1$9u6s7h+w2ljvn'

    # Configuration de l'email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'heritianajulien45@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'bysg pzyd umap fvog'  # À remplacer par un mot de passe d'application spécifique
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # Configurations supplémentaires
    DEBUG = os.environ.get('FLASK_DEBUG') or True  # Assurez-vous de mettre False en production

    # Paramètres de session
    SESSION_COOKIE_NAME = 'fete_session'  # Nom du cookie de session
    SESSION_TYPE = 'filesystem'  # Stockage de la session sur le système de fichiers
    SESSION_PERMANENT = False  # La session n'est pas permanente par défaut (elle expire à la fermeture du navigateur)
    SESSION_USE_SIGNER = True  # S'assurer que la session est signée pour plus de sécurité
    SESSION_COOKIE_SECURE = True  # Sécuriser le cookie (HTTPS uniquement, nécessaire en production)

    # Si tu veux utiliser la base de données pour stocker les sessions
    # SESSION_TYPE = 'sqlalchemy'
    # SESSION_SQLALCHEMY = db  # Assure-toi que `db` est défini comme la session SQLAlchemy

    # Configuration pour les cookies sécurisés (en production, nécessite HTTPS)
    SESSION_COOKIE_HTTPONLY = True  # Empêche l'accès au cookie de session via JavaScript
    SESSION_COOKIE_SAMESITE = 'Lax'  # Pour aider à la gestion des cookies cross-site

    # Utiliser un secret spécifique pour la session
    SESSION_SECRET_KEY = os.environ.get('SESSION_SECRET_KEY') or 'session_secret_key'
