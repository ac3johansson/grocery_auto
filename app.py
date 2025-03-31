from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from config import Config #Config file not created
from models import db
import os



def create_app():
    app = Flask(__name__)

    # Set a secret key (used for session security) 
    app.config['SECRET_KEY'] = os.urandom(24)  # Generates a random secret key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config.from_object(Config)  # Load config settings NOT CREATED

    #db = SQLAlchemy(app)
    db.init_app(app)  # Initialize database
    # Register Blueprint and import routes Blueprint
    from routes.routes import routes
    app.register_blueprint(routes)

    return app

app = create_app()

# # Import models AFTER initializing db
# from models.user import User
# from models.recipe import Recipe
# from models.ingredient import Ingredient
# from models.tag import Tag  

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


