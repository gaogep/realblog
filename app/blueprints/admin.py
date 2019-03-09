from flask import Blueprint
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)


# 为admin下的所有视图函数添加登录保护
@admin_bp.before_request
@login_required
def login_protect():
    pass
