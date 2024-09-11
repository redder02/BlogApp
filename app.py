from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes import auth_routes, post_routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(post_routes)


@app.route('/')
def base():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
