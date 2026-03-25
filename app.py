from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codebreaker.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    category = db.Column(db.String(50))
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    text = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        "id": p.id, "title": p.title, "content": p.content, "category": p.category,
        "likes": p.likes, "dislikes": p.dislikes, "comments": [c.text for c in p.comments]
    } for p in posts])

@app.route('/api/add_post', methods=['POST'])
def add_post():
    data = request.json
    if data.get('admin_code') == "CodeBreakerLearn12":
        new_p = Post(title=data['title'], content=data['content'], category=data['category'])
        db.session.add(new_p)
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

@app.route('/api/comment', methods=['POST'])
def add_comment():
    data = request.json
    new_c = Comment(post_id=data['id'], text=data['text'])
    db.session.add(new_c)
    db.session.commit()
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
