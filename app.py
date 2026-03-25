import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Путь к базе данных
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модели
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return jsonify([{"id": p.id, "title": p.title, "content": p.content, "category": p.category, "likes": p.likes, "dislikes": p.dislikes} for p in posts])

@app.route('/api/add', methods=['POST'])
def add():
    data = request.json
    if data.get('code') == "CodeBreakerLearn12":
        new_post = Post(title=data['title'], content=data['content'], category=data['category'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"status": "ok"}), 201
    return jsonify({"status": "error"}), 403

@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.json
    p = Post.query.get(data['id'])
    if data['type'] == 'like': p.likes += 1
    else: p.dislikes += 1
    db.session.commit()
    return jsonify({"l": p.likes, "d": p.dislikes})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
