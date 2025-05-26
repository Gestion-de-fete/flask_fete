from flask import request, jsonify
from models.client_model import db, Client
import qrcode
from io import BytesIO
import base64
from flask_mail import Message
from extensions import mail
import traceback
from PIL import Image
import qrcode.image.styledpil
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from datetime import datetime

def update_client(cin_client):
    try:
        # Récupérer le client existant par cin_client (clé primaire)
        client = Client.query.filter_by(cin_client=cin_client).first_or_404()

        # Récupérer les données du formulaire
        data = request.form

        # Vérifier si une nouvelle photo est fournie
        photo = request.files.get('photo_client')
        if photo:
            photo_data = photo.read()
        else:
            photo_data = client.photo_client  # Réutiliser la photo existante

        # Mettre à jour les champs du client, sauf cin_client (clé primaire)
        client.nom_client = data.get('nom_client', client.nom_client)
        client.prenom_client = data.get('prenom_client', client.prenom_client)
        client.email_client = data.get('email_client', client.email_client)
        client.adresse_client = data.get('adresse_client', client.adresse_client)
        client.telephone_client = data.get('telephone_client', client.telephone_client)
        client.paf_client = int(data.get('paf_client', client.paf_client))
        client.id_utilisateur = int(data.get('id_utilisateur', client.id_utilisateur))  # Clé étrangère
        client.photo_client = photo_data
        client.date_creation = datetime.utcnow() 

        # Construction du texte du QR code avec les données mises à jour
        qr_text = (
            f"CIN: {client.cin_client}\n"
            f"Nom: {client.nom_client}\n"
            f"Prénom: {client.prenom_client}\n"
            f"Email: {client.email_client}\n"
            f"Adresse: {client.adresse_client}\n"
            f"Téléphone: {client.telephone_client}\n"
            f"PAF: {client.paf_client}"
        )

        # Mettre à jour le texte du QR code dans la base de données
        client.codeqr_client = qr_text

        # Génération du QR code avec design amélioré
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)

        # Style personnalisé pour le QR code
        qr_image = qr.make_image(
            image_factory=qrcode.image.styledpil.StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 0, 0)),
            embeded_image_path=None
        )

        # Ouvrir la photo du client à partir des bytes
        client_photo = Image.open(BytesIO(photo_data))
        photo_size = (100, 100)  # Taille de la photo au centre
        client_photo = client_photo.resize(photo_size, Image.LANCZOS)

        # Calculer la position pour centrer la photo
        qr_width, qr_height = qr_image.size
        photo_width, photo_height = photo_size
        position = ((qr_width - photo_width) // 2, (qr_height - photo_height) // 2)

        # Coller la photo au centre du QR code
        qr_image.paste(client_photo, position)

        # Sauvegarder le QR code avec la photo dans un buffer
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        qr_code_bytes = buffer.getvalue()

        # Sauvegarder les modifications dans la base de données
        db.session.commit()

        # Envoi de l'email avec le nouveau QR code
        envoyer_email_client(client.email_client, qr_code_bytes)

        return jsonify({'message': 'Client modifié avec succès et nouveau QR code envoyé par email'}), 200

    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def envoyer_email_client(email, qr_code_bytes):
    msg = Message("Votre Code QR mis à jour", sender="ton.email@gmail.com", recipients=[email])
    msg.body = (
        "Bonjour,\n\n"
        "Vos informations ont été mises à jour. Vous trouverez en pièce jointe votre nouveau code QR personnalisé avec votre photo.\n"
        "Veuillez le conserver précieusement.\n\n"
        "Cordialement,\nL'équipe."
    )
    msg.attach("code_qr.png", "image/png", qr_code_bytes)
    mail.send(msg)