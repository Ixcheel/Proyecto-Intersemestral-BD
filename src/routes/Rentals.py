from flask import Blueprint, request, jsonify
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy import func

import src.extensions as db
from ..models.models import Rental, Customer, Staff, Inventory
from ..utils.Errors import reintentos
from ..config import Config

rentals_blueprint = Blueprint("rentals", __name__)


def make_session(isolation_level: str):
    session = db.SessionFactory()
    session.connection(execution_options={"isolation_level": isolation_level})
    return session


@rentals_blueprint.route("/rentals", methods=["POST"])
def crear_renta():
    data = request.get_json()
    customer_id = data.get("customer_id")
    inventory_id = data.get("inventory_id")
    staff_id = data.get("staff_id")

    def _do_create():
        session = make_session("REPEATABLE READ")
        try:
            inventory = (
                session.query(Inventory)
                .filter_by(inventory_id=inventory_id)
                .with_for_update(nowait=True).first()
            )

            rentado = (
                session.query(Rental).filter(
                    Rental.inventory_id == inventory_id,
                    Rental.return_date.is_(None)
                ).first()
            )

            if rentado:
                return jsonify({"error": "Está rentado"}), 409

            nueva_renta = Rental(
                inventory_id=inventory_id,
                customer_id=customer_id,
                staff_id=staff_id,
                rental_date=func.now(),
            )

            session.add(nueva_renta)
            session.commit()

            return jsonify({"rental_id": nueva_renta.rental_id}), 201

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return reintentos(_do_create, Config.MAX_RETRIES)