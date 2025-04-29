from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from models.utilisateur_model import db, Utilisateur
from flask_mail import Message
from extensions import mail

utilisateur_bp = Blueprint('utilisateur', __name__, url_prefix='/api/utilisateur')

# ➡️ Récupérer tous les utilisateurs
@utilisateur_bp.route('/', methods=['GET'])
def get_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return jsonify([
        {
            'id': u.id_utilisateur,
            'nom': u.nom_utilisateur,
            'prenom': u.prenom_utilisateur,
            'email': u.email_utilisateur,
            'role': u.role_utilisateur,
            'statut': u.statut_utilisateur
        }
        for u in utilisateurs
    ])

# ➡️ Créer un nouvel utilisateur
@utilisateur_bp.route('/', methods=['POST'])
def create_utilisateur():
    data = request.get_json()

    mot_de_passe_hache = generate_password_hash(data['mot_de_passe_utilisateur'])

    nouvel_utilisateur = Utilisateur(
        nom_utilisateur=data['nom_utilisateur'],
        prenom_utilisateur=data['prenom_utilisateur'],
        email_utilisateur=data['email_utilisateur'],
        role_utilisateur=data['role_utilisateur'],
        statut_utilisateur='en attente',
        mot_de_passe_utilisateur=mot_de_passe_hache
    )

    db.session.add(nouvel_utilisateur)
    db.session.commit()

    # Envoyer un email à l'administrateur
    envoyer_email_admin(nouvel_utilisateur)

    return jsonify({"message": "Inscription soumise pour validation par l'administrateur."}), 201

# ➡️ Valider ou refuser une inscription
@utilisateur_bp.route('/validation/<int:id_utilisateur>', methods=['PUT'])
def valider_utilisateur(id_utilisateur):
    data = request.get_json()
    statut = data.get('statut')

    if statut not in ['accepté', 'refusé']:
        return jsonify({'message': 'Statut invalide. Utilisez "accepté" ou "refusé".'}), 400

    utilisateur = Utilisateur.query.get(id_utilisateur)

    if not utilisateur:
        return jsonify({'message': 'Utilisateur non trouvé.'}), 404

    utilisateur.statut_utilisateur = statut
    db.session.commit()

    # Envoyer un email à l'utilisateur
    envoyer_email_utilisateur(utilisateur)

    return jsonify({'message': f'Utilisateur {statut} avec succès.'})

# ➡️ Route de login
@utilisateur_bp.route('/login', methods=['POST'])
def login_utilisateur():
    data = request.get_json()
    email = data.get('email_utilisateur')
    mot_de_passe = data.get('mot_de_passe_utilisateur')

    utilisateur = Utilisateur.query.filter_by(email_utilisateur=email).first()

    if utilisateur and check_password_hash(utilisateur.mot_de_passe_utilisateur, mot_de_passe):
        if utilisateur.statut_utilisateur != 'accepté':
            return jsonify({'message': 'Votre inscription n\'a pas été acceptée. Veuillez contacter l\'administrateur.'}), 403
        
        # Stocker les informations dans la session
        session['utilisateur_id'] = utilisateur.id_utilisateur
        session['role'] = utilisateur.role_utilisateur
        
        return jsonify({
            'message': 'Connexion réussie.',
            'id_utilisateur': utilisateur.id_utilisateur,
            'role_utilisateur': utilisateur.role_utilisateur
        }), 200

    return jsonify({'message': 'Email ou mot de passe incorrect.'}), 401

# ➡️ Route de logout (déconnexion)
@utilisateur_bp.route('/logout', methods=['POST'])
def logout_utilisateur():
    # Effacer toutes les informations de la session
    session.pop('utilisateur_id', None)
    session.pop('role', None) 
    # Marquer la session comme modifiée pour qu'elle soit enregistrée avec les modifications
    session.modified = True

    return jsonify({'message': 'Déconnexion réussie. La session a été terminée.'}), 200


# ➡️ Fonction pour envoyer un email à l'administrateur
def envoyer_email_admin(utilisateur):
    admin_email = 'heritianajulien45@gmail.com'

    msg = Message('Nouvelle demande d\'inscription',
                  recipients=[admin_email])

    msg.body = f"""\
Un nouvel utilisateur a demandé une inscription.

Nom : {utilisateur.nom_utilisateur}
Prénom : {utilisateur.prenom_utilisateur}
Email : {utilisateur.email_utilisateur}
Rôle : {utilisateur.role_utilisateur}

Merci de valider ou refuser cette inscription via l'interface d'administration.
"""
    mail.send(msg)

# ➡️ Fonction pour envoyer un email à l'utilisateur
def envoyer_email_utilisateur(utilisateur):
    msg = Message('Résultat de votre inscription',
                  recipients=[utilisateur.email_utilisateur])

    if utilisateur.statut_utilisateur == 'accepté':
        msg.body = f"""\
Bonjour {utilisateur.prenom_utilisateur},

Votre inscription a été acceptée ! 🎉
Vous pouvez maintenant vous connecter à la plateforme.

Merci et bienvenue !
"""
    else:
        msg.body = f"""\
Bonjour {utilisateur.prenom_utilisateur},

Nous sommes désolés, mais votre demande d'inscription a été refusée.

Pour plus d'informations, veuillez contacter l'administrateur.

Merci.
"""
    mail.send(msg)
