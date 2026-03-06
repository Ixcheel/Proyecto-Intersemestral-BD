from flask import Blueprint, request, jsonify
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DBAPIError
from .. import extensions
import time
import random

payments_blueprint = Blueprint("payments", __name__)

MAX_RETRIES = 5
ALLOWED_ISOLATION_LEVELS = {"READ COMMITTED", "SERIALIZABLE"}


@payments_blueprint.route("/payments", methods=["POST"])
def register_payment():
    data = request.get_json() or {}

    customer_id = data.get("customer_id")
    staff_id = data.get("staff_id")
    amount = data.get("amount")
    rental_id = data.get("rental_id", None)

    isolation_level = str(
        data.get("isolation_level", "READ COMMITTED")
    ).upper().strip()

    if isolation_level not in ALLOWED_ISOLATION_LEVELS:
        return jsonify({
            "error": "isolation_level inválido. Usa READ COMMITTED o SERIALIZABLE"
        }), 400

    if customer_id is None or staff_id is None or amount is None:
        return jsonify({
            "error": "customer_id, staff_id y amount son obligatorios"
        }), 400

    for attempt in range(MAX_RETRIES):
        session = None

        try:
            session = extensions.SessionFactory()
            if session is None:
                return jsonify({
                    "error": "SessionFactory no fue inicializado correctamente"
                }), 500

            session.execute(text(
                f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"
            ))

            payment_date = None

            if rental_id is not None:
                rental_row = session.execute(text("""
                    SELECT rental_id, customer_id, rental_date
                    FROM rental
                    WHERE rental_id = :rental_id
                """), {
                    "rental_id": rental_id
                }).fetchone()

                if not rental_row:
                    session.rollback()
                    session.close()
                    return jsonify({
                        "error": "Rental no existe"
                    }), 400

                if rental_row.customer_id != customer_id:
                    session.rollback()
                    session.close()
                    return jsonify({
                        "error": "Rental no existe o no pertenece al cliente"
                    }), 400

                payment_date = rental_row.rental_date

            else:
                # La base actual requiere rental_id NOT NULL.
                session.rollback()
                session.close()
                return jsonify({
                    "error": "No se puede registrar el pago porque debe estar asociado a una renta (rental_id)"
                }), 400

            session.execute(text("""
                INSERT INTO payment (
                    customer_id,
                    staff_id,
                    rental_id,
                    amount,
                    payment_date
                )
                VALUES (
                    :customer_id,
                    :staff_id,
                    :rental_id,
                    :amount,
                    :payment_date
                )
            """), {
                "customer_id": customer_id,
                "staff_id": staff_id,
                "rental_id": rental_id,
                "amount": amount,
                "payment_date": payment_date
            })

            session.commit()
            session.close()

            response = {
                "message": "Payment registrado correctamente",
                "customer_id": customer_id,
                "staff_id": staff_id,
                "amount": amount
            }

            if rental_id is not None:
                response["rental_id"] = rental_id

            return jsonify(response), 200

        except (OperationalError, DBAPIError) as e:
            if session is not None:
                session.rollback()
                session.close()

            error_text = str(e).lower()

            if "deadlock detected" in error_text or "serialization failure" in error_text:
                sleep_time = (2 ** attempt) + random.random()
                time.sleep(sleep_time)
                continue

            return jsonify({
                "error": str(e)
            }), 500

        except Exception as e:
            if session is not None:
                session.rollback()
                session.close()

            return jsonify({
                "error": str(e)
            }), 500

    return jsonify({
        "error": "Transaction failed after retries"
    }), 500