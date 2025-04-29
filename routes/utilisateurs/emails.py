from flask_mail import Message
from extensions import mail

def envoyer_email_admin(utilisateur):
    msg = Message('Nouvelle demande d\'inscription',
                  recipients=['heritianajulien45@gmail.com'])
    msg.body = f"""
Un nouvel utilisateur a demandé une inscription.

Nom : {utilisateur.nom_utilisateur}
Prénom : {utilisateur.prenom_utilisateur}
Email : {utilisateur.email_utilisateur}
Rôle : {utilisateur.role_utilisateur}

Merci de valider ou refuser cette inscription via l'interface d'administration.
"""
    mail.send(msg)

def envoyer_email_utilisateur(utilisateur, statut):
    msg = Message('Résultat de votre inscription',
                  recipients=[utilisateur.email_utilisateur])
    if statut == 'accepté':
        msg.body = f"""
Bonjour {utilisateur.prenom_utilisateur},

Votre inscription a été acceptée ! 🎉
Vous pouvez maintenant vous connecter à la plateforme.

Merci et bienvenue !
"""
    else:
        msg.body = f"""
Bonjour {utilisateur.prenom_utilisateur},

Nous sommes désolés, mais votre demande d'inscription a été refusée.

Pour plus d'informations, veuillez contacter l'administrateur.

Merci.
"""
    mail.send(msg)
