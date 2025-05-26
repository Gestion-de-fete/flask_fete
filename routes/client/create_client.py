from flask import request, jsonify
from datetime import datetime
from io import BytesIO
import traceback
import qrcode
from PIL import Image
import qrcode.image.styledpil
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from flask_mail import Message

from models.client_model import db, Client
from models.entree_sortie_model import EntreeSortie
from extensions import mail

def create_client():
    try:
        data = request.form
        photo = request.files['photo_client'].read()

        # Construction du texte du QR code
        qr_text = (
            f"CIN: {data['cin_client']}\n"
            f"Nom: {data['nom_client']}\n"
            f"Prénom: {data['prenom_client']}\n"
            f"Email: {data['email_client']}\n"
            f"Adresse: {data['adresse_client']}\n"
            f"Téléphone: {data['telephone_client']}\n"
            f"PAF: {data['paf_client']}"
        )

        # Génération du QR code stylisé
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)

        qr_image = qr.make_image(
            image_factory=qrcode.image.styledpil.StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 0, 0)),
            embeded_image_path=None
        )

        client_photo = Image.open(BytesIO(photo))
        client_photo = client_photo.resize((100, 100), Image.LANCZOS)
        qr_width, qr_height = qr_image.size
        position = ((qr_width - 100) // 2, (qr_height - 100) // 2)
        qr_image.paste(client_photo, position)

        # Sauvegarde en mémoire
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        qr_code_bytes = buffer.getvalue()

        # Création du client
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
            codeqr_client=qr_text,
                date_creation=datetime.utcnow() 
        )
        db.session.add(new_client)
        db.session.commit()

        # Insertion dans la table EntreeSortie avec état = 'sortie'
        sortie = EntreeSortie(
            cin_client=new_client.cin_client,
            etat='sortie',
            date_heure=datetime.utcnow()
        )
        db.session.add(sortie)
        db.session.commit()

        # Envoi de l'e-mail avec QR code
        envoyer_email_client(data['email_client'], qr_code_bytes)

        return jsonify({'message': 'Client ajouté avec succès, QR code envoyé par email, et sortie enregistrée.'}), 201

    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def envoyer_email_client(email, qr_code_bytes):
    msg = Message(
        subject="Votre Code QR d'inscription",
        sender="ton.email@gmail.com",
        recipients=[email]
    )
    msg.body = (
        "Bonjour,\n\n"
        "Merci pour votre inscription. Vous trouverez en pièce jointe votre code QR personnalisé avec votre photo.\n"
        "Veuillez le conserver précieusement.\n\n"
        "Cordialement,\nL'équipe."
    )
    msg.attach("code_qr.png", "image/png", qr_code_bytes)
    mail.send(msg)
