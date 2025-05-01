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

def create_client():
    try:
        data = request.form
        photo = request.files['photo_client'].read()

        # Construction du texte du QR code avec toutes les données
        qr_text = (
            f"CIN: {data['cin_client']}\n"
            f"Nom: {data['nom_client']}\n"
            f"Prénom: {data['prenom_client']}\n"
            f"Email: {data['email_client']}\n"
            f"Adresse: {data['adresse_client']}\n"
            f"Téléphone: {data['telephone_client']}\n"
            f"PAF: {data['paf_client']}"
        )

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
            color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 0, 255)),
            embeded_image_path=None
        )

        # Ouvrir la photo du client à partir des bytes
        client_photo = Image.open(BytesIO(photo))
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

        # Sauvegarde dans la base de données
        new_client = Client(
            cin_client=data['cin_client'],
            id_utilisateur=int(data['id_utilisateur']),
            photo_client=photo,
            nom_client=data['nom_client'],
            prenom_client=data['prenom_client'],
            email_client=data['email_client'],
            adresse_client=data['adresse_client'],
            telephone_client=data['telephone_client'],
            paf_client=int(data['paf_client']),
            codeqr_client=qr_text
        )

        db.session.add(new_client)
        db.session.commit()

        # Envoi de l'email avec QR code
        envoyer_email_client(data['email_client'], qr_code_bytes)

        return jsonify({'message': 'Client ajouté avec succès et QR code envoyé par email'}), 201

    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def envoyer_email_client(email, qr_code_bytes):
    msg = Message("Votre Code QR d'inscription", sender="ton.email@gmail.com", recipients=[email])
    msg.body = (
        "Bonjour,\n\n"
        "Merci pour votre inscription. Vous trouverez en pièce jointe votre code QR personnalisé avec votre photo.\n"
        "Veuillez le conserver précieusement.\n\n"
        "Cordialement,\nL'équipe."
    )
    msg.attach("code_qr.png", "image/png", qr_code_bytes)
    mail.send(msg)