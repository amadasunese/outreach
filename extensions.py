from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bootstrap = Bootstrap()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()