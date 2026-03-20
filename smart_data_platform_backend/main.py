# main.py - 系统入口，负责系统初始化和服务启动

from flask import Flask
from flask_cors import CORS
# from app.api.product_api import product_bp
# from app.api.comment_api import comment_bp
from app.api.crawler_api import crawler_bp
from app.api.analysis_api import analysis_bp
from app.api.login import login_bp


def create_app():
    """
    创建Flask应用实例，初始化系统模块
    """
    app = Flask(__name__)

    # 启用跨域支持
    CORS(app)

    # 注册API蓝图 - API接口层
    app.register_blueprint(login_bp, url_prefix='/api')
    # app.register_blueprint(product_bp, url_prefix='/api')
    # app.register_blueprint(comment_bp, url_prefix='/api')
    app.register_blueprint(crawler_bp, url_prefix='/api')
    app.register_blueprint(analysis_bp, url_prefix='/api')

    return app


if __name__ == "__main__":

    app = create_app()

    app.run(port=5000, debug=True)


