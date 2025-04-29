from flask import Flask
from config import Config
from models._init_ import db
from routes.__init__ import create_routes
from extensions import mail

from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"],
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Charger la config principale
app.config.from_object(Config)

# Initialiser extensions
db.init_app(app)
mail.init_app(app)

# Créer toutes les tables
with app.app_context():
    db.create_all()

# Enregistrer les blueprints (routes)
create_routes(app)

@app.route('/')
def index():
    return 'Welcome to the Flask Application!'

if __name__ == '__main__':
    app.run(debug=True)
