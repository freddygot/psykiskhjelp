from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Importer Migrate-klassen
from models import db
from routes import routes
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)


    with app.app_context():
        db.create_all()  # Oppretter databasetabeller

    app.register_blueprint(routes)
    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
