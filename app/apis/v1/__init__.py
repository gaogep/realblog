from flask import Blueprint
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)
CORS(api_v1)  # 添加CORS支持

from app.apis.v1 import resources  # 导入资源模块 关联蓝本与视图

