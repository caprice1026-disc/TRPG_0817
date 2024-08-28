from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Hello, TRPG!"

if __name__ == "__main__":
    app.run(debug=True)
