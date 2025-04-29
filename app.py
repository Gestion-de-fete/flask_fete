from flask import Flask
from config import Config
from models._init_ import db
from routes.__init__ import create_routes
from extensions import mail

app = Flask(__name__)

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
