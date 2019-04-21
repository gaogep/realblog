from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_whooshee import Whooshee
from flask_debugtoolbar import DebugToolbarExtension


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
moment = Moment()
pagedown = PageDown()
whooshee = Whooshee()
# toolbar = DebugToolbarExtension()


@login_manager.user_loader
def get_user(user_id):
    from .models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'warning'

