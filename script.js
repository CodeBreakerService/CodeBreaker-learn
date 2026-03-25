// Анимация фона (код)
const canvas = document.getElementById('bg-code');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth; canvas.height = window.innerHeight;

const codes = ['const app = Flask()', 'def build():', '<html>', 'margin: 0;', 'db.create_all()', 'print("Success")'];
let items = Array.from({length: 30}, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    txt: codes[Math.floor(Math.random() * codes.length)],
    v: 0.4 + Math.random()
}));

function draw() {
    ctx.clearRect(0,0,canvas.width, canvas.height);
    ctx.font = "14px 'Fira Code'";
    ctx.fillStyle = "#cbd5e1";
    items.forEach(i => {
        ctx.fillText(i.txt, i.x, i.y);
        i.y -= i.v; if(i.y < -20) i.y = canvas.height + 20;
    });
    requestAnimationFrame(draw);
}
draw();

// Функции профиля
function openModal() { document.getElementById('modal-bg').style.display = 'block'; }
function closeModal() { document.getElementById('modal-bg').style.display = 'none'; }

function saveProfile() {
    const name = document.getElementById('in-name').value;
    const code = document.getElementById('in-code').value;
    if(name) document.getElementById('u-name').innerHTML = `<span class="material-icons">check_circle</span> ${name}`;
    if(code === "CodeBreakerLearn12") {
        document.getElementById('admin-panel').style.display = 'block';
    }
    closeModal();
}

// Загрузка постов
async function loadPosts() {
    const r = await fetch('/api/posts');
    const posts = await r.json();
    const feed = document.getElementById('posts-feed');
    feed.innerHTML = posts.map(p => `
        <div class="card">
            <span class="post-cat">${p.category}</span>
            <h2>${p.title}</h2>
            <p style="white-space: pre-wrap;">${p.content}</p>
            <div style="display:flex; gap:10px; border-top:1px solid #eee; padding-top:15px;">
                <button class="btn-icon" onclick="vote(${p.id}, 'like')"><span class="material-icons">thumb_up</span> ${p.likes}</button>
                <button class="btn-icon" onclick="vote(${p.id}, 'dislike')"><span class="material-icons">thumb_down</span> ${p.dislikes}</button>
            </div>
        </div>
    `).join('');
}

async function publish() {
    const data = {
        title: document.getElementById('p-title').value,
        category: document.getElementById('p-cat').value,
        content: document.getElementById('p-content').value,
        code: document.getElementById('in-code').value
    };
    await fetch('/api/add', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});
    loadPosts();
}

async function vote(id, type) {
    await fetch('/api/vote', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, type})});
    loadPosts();
}

loadPosts();
