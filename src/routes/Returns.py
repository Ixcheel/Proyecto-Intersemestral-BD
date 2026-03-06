
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy import func

import src.extensions as db
from ..models.models import Rental
from ..utils.Errors import reintentos
from ..config import Config


returns_blueprint = Blueprint("returns", __name__)

def make_session(isolation_level: str):
    session = db.SessionFactory()
    session.connection(execution_options={"isolation_level": isolation_level})
    return session

@returns_blueprint.route("/returns/<int:rental_id>", methods=["POST"])
def crear_retunrs():
    
    def _do_create():
        session = make_session("SERIALIZABLE")
        try:
            renta = (
                session.query(Rental)
                .filter_by(rental_id=rental_id)
                .with_for_update().first()
            )

            if not renta:
                return jsonify({"error": "No se encontro la renta"}), 409

            if renta.return_date is not None:
                return jsonify({"message": "Esta devolución ya ha sido registrada ", "return_date": renta.return_date}), 200

           
            renta.return_date = func.now()
            session.commit()

            return jsonify({"message": "Devolución registrada"}), 200

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return reintentos(_do_create, Config.MAX_RETRIES)
    