from flask import Flask, jsonify,Response,sse
from flask_sqlalchemy import SQLAlchemy
from models import db
import time

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Hello, TRPG!"

clients = []

@app.route('/events')
def events():
    def eventStream():
        while True:
            # データ変更を監視するロジックをここに追加
            if clients:
                yield f"data: {jsonify({'message': 'データが更新されました'})}\n\n"
            time.sleep(1)  # ポーリング間隔

    return Response(eventStream(), content_type='text/event-stream')

@app.route('/update', methods=['POST'])
def update():
    # データの更新処理
    # 例: データベースの更新など
    global clients
    clients.append('new_update')
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
