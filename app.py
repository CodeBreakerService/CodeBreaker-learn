import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, 
            template_folder='templates', 
            static_folder='static')

# База данных
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'codebreaker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ADMIN_SECRET = "CodeBreakerLearn12"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return jsonify([{
        "id": p.id, "title": p.title, "content": p.content, "category": p.category,
        "likes": p.likes, "dislikes": p.dislikes, "comments": [c.text for c in p.comments]
    } for p in posts])

@app.route('/api/add_post', methods=['POST'])
def add_post():
    data = request.json
    if data.get('admin_code') == ADMIN_SECRET:
        new_p = Post(title=data['title'], content=data['content'], category=data['category'])
        db.session.add(new_p)
        db.session.commit()
        return jsonify({"status": "success"}), 201
    return jsonify({"status": "unauthorized"}), 403

@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.json
    p = Post.query.get(data['id'])
    if data['type'] == 'like': p.likes += 1
    else: p.dislikes += 1
    db.session.commit()
    return jsonify({"likes": p.likes, "dislikes": p.dislikes})

@app.route('/api/comment', methods=['POST'])
def add_comment():
    data = request.json
    new_c = Comment(post_id=data['id'], text=data['text'])
    db.session.add(new_c)
    db.session.commit()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Берем порт из переменной окружения или ставим 10000 по умолчанию
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
