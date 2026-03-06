from flask import Flask
from .config import Config
from .extensions import db,migrate, init_db
from .routes.Rentals import rentals_blueprint
from .models.models import Inventory, Rental

def create_app():
    app = Flask(__name__)
    init_db(Config.DATABASE_URL)

    app.register_blueprint(rentals_blueprint)
    app.register_blueprint(returns_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)