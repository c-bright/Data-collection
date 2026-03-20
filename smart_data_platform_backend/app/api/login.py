from flask import jsonify, Blueprint, request
from app.utils.database.db_manager import DatabaseManager
from app.models.user_model import User
import traceback

# 定义蓝图，统一前缀为 /api
login_bp = Blueprint("login", __name__, url_prefix="/api")


@login_bp.route("/register", methods=["POST"])
def register():
    """
    用户注册接口
    逻辑：主动检查用户名冲突；不主动检查邮箱，但捕获数据库 Unique 约束冲突。
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    # 1. 基础字段校验
    if not username or not password or not email:
        return jsonify(success=False, message="字段不能为空"), 400

    db_manager = DatabaseManager()
    session = db_manager.get_session()

    try:
        # 2. 【主动检查】仅检查用户名是否重复
        existing_user = session.query(User).filter(User.username == username).first()
        if existing_user:
            return jsonify(success=False, message="该用户名已被占用"), 409

        # 3. 创建新用户对象
        # 注意：此处未对密码进行哈希加密，直接存储明文（按当前需求执行）
        new_user = User(
            username=username,
            password=password,
            email=email
        )

        session.add(new_user)
        # 4. 提交到数据库
        # 如果 email 在数据库中已存在，此处会抛出 IntegrityError
        session.commit()

        return jsonify(success=True, message="注册成功"), 200

    except Exception as e:
        session.rollback()  # 发生任何异常立即回滚事务

        error_msg = str(e)
        # 5. 【被动捕获】检查是否为数据库层面的 Email 唯一性冲突
        if "Duplicate entry" in error_msg and "user.email" in error_msg:
            return jsonify(success=False, message="该邮箱已被其他账号绑定"), 409

        print("[REGISTER] 捕获未预期异常:")
        traceback.print_exc()
        return jsonify(success=False, message=f"注册失败: {error_msg}"), 500
    finally:
        # 释放 Session 资源
        db_manager.Session.remove()


@login_bp.route("/login", methods=["POST"])
def login():
    """
    用户登录接口
    逻辑：根据用户名查询，匹配明文密码。
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(success=False, message="字段不能为空"), 400

    db_manager = DatabaseManager()
    session = db_manager.get_session()

    try:
        # 1. 使用 ORM 查询用户
        user = session.query(User).filter(User.username == username).first()

        if not user:
            return jsonify(success=False, message="用户不存在"), 404

        # 2. 验证明文密码
        if user.password != password:
            return jsonify(success=False, message="密码错误"), 401

        # 3. 登录成功，利用模型中的 to_dict() 返回脱敏后的用户信息
        return jsonify({
            "success": True,
            "message": "登录成功",
            "user": user.to_dict()
        }), 200

    except Exception as e:
        print("[LOGIN] 捕获异常:")
        traceback.print_exc()
        return jsonify(success=False, message=str(e)), 500
    finally:
        db_manager.Session.remove()