from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_moment import Moment

from .models import User


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
moment = Moment()


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
