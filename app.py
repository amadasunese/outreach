# from flask import Flask
# from extensions import db
# from config import Config
# from flask_login import LoginManager
# from extensions import db, migrate, login_manager, bootstrap
# from views import auth
# from models import User
# # from flaskwebgui import FlaskUI


# app = Flask(__name__)
# app.config.from_object(Config)

# # ui = FlaskUI(app, width=500, height=500) 

# db.init_app(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'auth.login'
# migrate.init_app(app, db)
# bootstrap.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# app.register_blueprint(auth) # url_prefix='/auth')


# # from views import *

# # Register blueprints
# from models import *

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
#     # ui.run()

from flask import Flask
from extensions import db, migrate, login_manager, bootstrap
from config import Config
from flask_migrate import upgrade
from views import auth
from models import *  # Ensure all models are imported

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
with app.app_context():
    upgrade()  # Auto-applies any new migrations

if __name__ == '__main__':
    app.run(debug=True)

