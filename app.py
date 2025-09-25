from flask import Flask
from extensions import db, migrate, login_manager, bootstrap
from config import Config
from flask_migrate import upgrade
from views import auth
from models import User

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
bootstrap.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth)

# Automatically apply migrations on startup
# with app.app_context():
#     upgrade()  # Auto-applies any new migrations

if __name__ == '__main__':
    app.run(debug=True)

