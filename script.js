const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth; canvas.height = window.innerHeight;

const codes = ['<div>', 'console.log()', 'def main():', 'color: #fff;', 'npm install', 'push()', 'class User:'];
let particles = Array.from({length: 40}, () => ({
    x: Math.random() * canvas.width, y: Math.random() * canvas.height,
    text: codes[Math.floor(Math.random() * codes.length)], s: 0.5 + Math.random()
}));

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#000"; ctx.font = "14px Fira Code";
    particles.forEach(p => {
        ctx.fillText(p.text, p.x, p.y);
        p.y -= p.s; if(p.y < -20) p.y = canvas.height + 20;
    });
    requestAnimationFrame(draw);
}
draw();

function toggleModal(show) { document.getElementById('profile-modal').style.display = show ? 'block' : 'none'; }

function saveProfile() {
    const name = document.getElementById('name-in').value;
    const code = document.getElementById('code-in').value;
    if(name) document.getElementById('user-name').innerHTML = `<span class="material-icons">verified</span> ${name}`;
    if(code === "CodeBreakerLearn12") document.getElementById('admin-panel').style.display = 'block';
    toggleModal(false);
}

async function loadPosts() {
    const res = await fetch('/api/posts');
    const data = await res.json();
    const feed = document.getElementById('feed');
    feed.innerHTML = data.map(p => `
        <div class="card">
            <div class="tag"><span class="material-icons">label</span> ${p.category}</div>
            <h2><span class="material-icons">menu_book</span> ${p.title}</h2>
            <p>${p.content}</p>
            <div class="actions">
                <button onclick="vote(${p.id}, 'like')"><span class="material-icons">thumb_up</span> <span>${p.likes}</span></button>
                <button onclick="vote(${p.id}, 'dislike')"><span class="material-icons">thumb_down</span> <span>${p.dislikes}</span></button>
                <button onclick="addCom(${p.id})"><span class="material-icons">comment</span> <span>${p.comments.length}</span></button>
            </div>
        </div>
    `).join('');
}

async function sendPost() {
    const body = {
        title: document.getElementById('post-title').value,
        category: document.getElementById('post-cat').value,
        content: document.getElementById('post-text').value,
        admin_code: document.getElementById('code-in').value
    };
    await fetch('/api/add_post', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
    loadPosts();
}

async function vote(id, type) {
    await fetch('/api/vote', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, type})});
    loadPosts();
}

loadPosts();
