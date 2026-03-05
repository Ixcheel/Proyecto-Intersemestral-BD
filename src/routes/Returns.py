from flask import Blueprint, request, jsonify
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy import func

import src.extensions as db
from ..models.models import 
from ..utils.Errors import with_retry
from ..config import Config

returns_blueprint = Blueprint("returns", __name__)

def make_session(isolation_level: str):
    session = db.SessionFactory()
    session.connection(execution_options={"isolation_level": isolation_level})
    return session


@returns_blueprint.route("/returns/<rental_id>", methods=["POST"])
def crear_retunrs():
    data = request.get_json()
    ## Datos que tengo que obtener
    
    def _do_create():
        session = make_session("READ COMMITED")
        # Logica

