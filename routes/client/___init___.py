from flask import Blueprint
from .create_client import create_client
from .update_client import update_client
from .delete_client import delete_client
from .get_client import get_client
from .list_client_2_date import filtrer_clients_par_date

client_bp = Blueprint('client', __name__, url_prefix='/api/client')

client_bp.route('/create', methods=['POST'])(create_client)
client_bp.route('/fetch', methods=['GET'])(get_client)
client_bp.route('/update/<string:cin_client>', methods=['PUT'])(update_client)
client_bp.route('/delete/<string:cin_client>', methods=['DELETE'])(delete_client)
client_bp.route('/list', methods=['GET'])(filtrer_clients_par_date)
