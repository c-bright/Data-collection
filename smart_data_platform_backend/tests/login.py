# test_backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"收到登录请求: {data}")
    return jsonify({
        'success': True,
        'message': '登录成功',
        'token': 'mock-token-123',
        'user': {'username': data['username']}
    })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    print(f"收到注册请求: {data}")
    return jsonify({
        'success': True,
        'message': '注册成功'
    })

if __name__ == '__main__':
    print("后端服务启动在 http://127.0.0.1:5000")
    app.run(debug=True, port=5000)