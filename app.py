from flask import Flask, render_template_string

app = Flask(__name__)

# Minimal Main HTML - CTRL + U (View Source) par sirf yeh dikhega
MAIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexura</title>
</head>
<body style="background-color: #090014; margin: 0;">

    <div id="nexura-app"></div>

    <script>
        // Backend API se UI components aur design fetch ho kar yahan inject hongay
        fetch('./api/render-ui')
            .then(response => {
                if (!response.ok) throw new Error('HTTP status ' + response.status);
                return response.text();
            })
            .then(htmlContent => {
                document.getElementById('nexura-app').innerHTML = htmlContent;
            })
            .catch(err => console.error('Error loading UI:', err));
    </script>

</body>
</html>"""

# Complete JoyMix Application UI & Styles (Backend Component)
BACKEND_UI_COMPONENT = """<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

    :root {
        --bg-color: #0f0f0f;
        --card-bg: #181818;
        --text-color: #f1f1f1;
        --subtext-color: #aaa;
        --border-color: rgba(255, 255, 255, 0.1);
        --chip-bg: rgba(255, 255, 255, 0.1);
        --chip-hover-bg: #f1f1f1;
        --chip-hover-text: #0f0f0f;
        --shadow-color: rgba(0, 0, 0, 0.6);
    }

    body.light-theme {
        --bg-color: #ffffff;
        --card-bg: #f9f9f9;
        --text-color: #0f0f0f;
        --subtext-color: #606060;
        --border-color: rgba(0, 0, 0, 0.1);
        --chip-bg: rgba(0, 0, 0, 0.05);
        --chip-hover-bg: #0f0f0f;
        --chip-hover-text: #ffffff;
        --shadow-color: rgba(0, 0, 0, 0.15);
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
        user-select: none;
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    .joymix-wrapper {
        background-color: var(--bg-color);
        color: var(--text-color);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        overflow-x: hidden;
    }

    /* Header */
    header {
        width: 100%;
        height: 60px;
        background: var(--bg-color);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
        position: sticky;
        top: 0;
        z-index: 100;
        border-bottom: 1px solid var(--border-color);
    }

    .logo-box {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 22px;
        font-weight: 700;
        color: var(--text-color);
        letter-spacing: -0.5px;
        cursor: pointer;
        text-decoration: none;
    }

    .logo-icon {
        color: #ff0000;
        font-size: 26px;
    }

    .header-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .theme-toggle-btn {
        background: var(--chip-bg);
        color: var(--text-color);
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border: 1px solid var(--border-color);
        font-size: 18px;
    }

    .creator-link {
        background: var(--chip-bg);
        color: var(--text-color);
        padding: 8px 16px;
        border-radius: 20px;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        border: 1px solid var(--border-color);
    }

    .creator-link:hover {
        background: #ff0000;
        color: #fff;
        border-color: #ff0000;
    }

    /* Category Filter Bar */
    .category-bar {
        width: 100%;
        padding: 12px 20px;
        background: var(--bg-color);
        display: flex;
        gap: 12px;
        overflow-x: auto;
        position: sticky;
        top: 60px;
        z-index: 90;
        border-bottom: 1px solid var(--border-color);
    }

    .category-bar::-webkit-scrollbar {
        display: none;
    }

    .chip {
        background: var(--chip-bg);
        color: var(--text-color);
        padding: 8px 18px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 500;
        white-space: nowrap;
        cursor: pointer;
        border: none;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .chip.active, .chip:hover {
        background: var(--chip-hover-bg);
        color: var(--chip-hover-text);
    }

    /* Feed Grid */
    main {
        padding: 20px;
        max-width: 1600px;
        margin: 0 auto;
        width: 100%;
    }

    .grid-feed {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 20px;
    }

    .card {
        background: var(--card-bg);
        border-radius: 16px;
        overflow: hidden;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        border: 1px solid var(--border-color);
    }

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px var(--shadow-color);
    }

    .thumbnail {
        width: 100%;
        height: 180px;
        background-size: cover;
        background-position: center;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(128, 128, 128, 0.2);
    }

    .thumbnail i.play-icon {
        font-size: 48px;
        color: #ff0000;
        filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));
    }

    .badge {
        position: absolute;
        bottom: 10px;
        right: 10px;
        background: rgba(0, 0, 0, 0.85);
        color: #fff;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .card-details {
        padding: 14px;
        display: flex;
        gap: 12px;
    }

    .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: var(--chip-bg);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        color: var(--text-color);
        flex-shrink: 0;
    }

    .info h3 {
        font-size: 15px;
        font-weight: 600;
        color: var(--text-color);
        line-height: 1.3;
        margin-bottom: 4px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .info p {
        font-size: 13px;
        color: var(--subtext-color);
    }

    /* Mobile Fullscreen Viewer */
    .player-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: #000;
        z-index: 1000;
        justify-content: center;
        align-items: center;
    }

    .player-container {
        width: 100vw;
        height: 100vh;
        position: relative;
        overflow: hidden;
    }

    .controls-overlay {
        position: absolute;
        top: 15px;
        right: 15px;
        display: flex;
        gap: 12px;
        z-index: 1001;
    }

    .action-btn {
        color: #fff;
        font-size: 16px;
        cursor: pointer;
        background: rgba(0, 0, 0, 0.7);
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }

    .action-btn:active {
        transform: scale(0.9);
        background: #ff0000;
    }

    iframe {
        width: 100%;
        height: 100%;
        border: none;
    }
</style>

<div class="joymix-wrapper">
    <header>
        <a href="2.html" class="logo-box">
            <i class="fa-brands fa-youtube logo-icon"></i> JoyMix
        </a>
        <div class="header-actions">
            <div class="theme-toggle-btn" onclick="toggleTheme()" title="Toggle Dark/Light Mode">
                <i class="fa-solid fa-moon" id="themeIcon"></i>
            </div>
            <a href="2.html" class="creator-link">
                <i class="fa-solid fa-circle-user"></i> Created by Muhammad Taqi
            </a>
        </div>
    </header>

    <div class="category-bar">
        <button class="chip active" onclick="filterCategory('all', this)"><i class="fa-solid fa-house"></i> All</button>
        <button class="chip" onclick="filterCategory('games', this)"><i class="fa-solid fa-gamepad"></i> Games</button>
        <button class="chip" onclick="filterCategory('videos', this)"><i class="fa-solid fa-film"></i> Videos</button>
        <button class="chip" onclick="filterCategory('images', this)"><i class="fa-solid fa-image"></i> Images</button>
        <button class="chip" onclick="filterCategory('poetry', this)"><i class="fa-solid fa-feather"></i> Poetry</button>
    </div>

    <main>
        <div class="grid-feed" id="feedGrid"></div>
    </main>

    <div class="player-modal" id="playerModal">
        <div class="player-container">
            <div class="controls-overlay">
                <span class="action-btn" id="prevBtn" onclick="prevVideo()" style="display: none;" title="Previous Video">
                    <i class="fa-solid fa-arrow-left"></i>
                </span>
                <span class="action-btn" id="nextBtn" onclick="nextVideo()" style="display: none;" title="Next Video">
                    <i class="fa-solid fa-arrow-right"></i>
                </span>
                <span class="action-btn" onclick="closePlayer()" title="Close">
                    <i class="fa-solid fa-xmark"></i>
                </span>
            </div>
            <iframe id="mainFrame" src="" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>
    </div>
</div>

<script>
    let videoQueue = [];
    let currentVideoIndex = -1;

    const staticItems = [
        { type: 'games', title: '50 Game Classic', path: 'https://muhammadtaqi512q-oss.github.io/video/games/50.html', icon: 'fa-trophy', bg: 'fa-gamepad' },
        { type: 'games', title: 'Flappy Bird Arcade', path: 'https://muhammadtaqi512q-oss.github.io/video/games/Flappy-Bird.html', icon: 'fa-dove', bg: 'fa-crow' },
        { type: 'games', title: 'Hill Climb Racing', path: 'https://muhammadtaqi512q-oss.github.io/video/games/Hill-Climb.html', icon: 'fa-truck', bg: 'fa-car' },
        { type: 'games', title: 'Dino Runner v1', path: 'https://muhammadtaqi512q-oss.github.io/video/games/diano1.html', icon: 'fa-paw', bg: 'fa-dragon' },
        { type: 'games', title: 'Dino Runner v2', path: 'https://muhammadtaqi512q-oss.github.io/video/games/diano2.html', icon: 'fa-dragon', bg: 'fa-dragon' },
        { type: 'games', title: 'Ludo Star Online', path: 'https://muhammadtaqi512q-oss.github.io/video/games/ludo.html', icon: 'fa-dice-four', bg: 'fa-dice' },
        { type: 'games', title: 'Stickman Hero', path: 'https://muhammadtaqi512q-oss.github.io/video/games/stickman.html', icon: 'fa-user-ninja', bg: 'fa-person-running' },
        { type: 'games', title: 'Rock Paper Scissors', path: 'https://muhammadtaqi512q-oss.github.io/video/games/stone-paper-seasor.html', icon: 'fa-hand-back-fist', bg: 'fa-hand' },
        { type: 'games', title: 'Tic Tac Toe Pro v2', path: 'https://muhammadtaqi512q-oss.github.io/video/games/tic-cros-2.html', icon: 'fa-xmark', bg: 'fa-hashtag' },
        { type: 'games', title: 'Tic Tac Toe Classic', path: 'https://muhammadtaqi512q-oss.github.io/video/games/tic-cross.html', icon: 'fa-grip-lines', bg: 'fa-table-cells' },
        { type: 'images', title: 'Online Gallery Stream', path: 'https://muhammadtaqi512q-oss.github.io/video/image/online.html', icon: 'fa-camera', bg: 'fa-globe' },
        { type: 'poetry', title: 'Poetry Cards & Quotes', path: 'https://muhammadtaqi512q-oss.github.io/video/image/poetry.html', icon: 'fa-book-open', bg: 'fa-feather' },
        { type: 'images', title: 'Offline Image Storage', path: 'https://muhammadtaqi512q-oss.github.io/video/image/offline.html', icon: 'fa-box-archive', bg: 'fa-hard-drive' }
    ];

    function extractVideoID(urlOrId) {
        const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        const match = urlOrId.match(regExp);
        return (match && match[2].length === 11) ? match[2] : urlOrId;
    }

    function toggleTheme() {
        const body = document.body;
        const icon = document.getElementById('themeIcon');
        body.classList.toggle('light-theme');
        icon.className = body.classList.contains('light-theme') ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    }

    function loadFeed() {
        const grid = document.getElementById('feedGrid');
        if (!grid) return;
        let allCards = [];

        if (typeof videoLinks !== 'undefined' && Array.isArray(videoLinks)) {
            videoQueue = videoLinks.map(item => extractVideoID(item));
        }

        staticItems.forEach(item => {
            allCards.push({
                category: item.type,
                html: `
                    <div class="card item-${item.type}" onclick="playDirectItem('${item.path}')">
                        <div class="thumbnail">
                            <i class="fa-solid ${item.bg} play-icon"></i>
                            <span class="badge">${item.type.toUpperCase()}</span>
                        </div>
                        <div class="card-details">
                            <div class="avatar"><i class="fa-solid ${item.icon}"></i></div>
                            <div class="info">
                                <h3>${item.title}</h3>
                                <p>JoyMix • Play Now</p>
                            </div>
                        </div>
                    </div>`
            });
        });

        videoQueue.forEach((vid, index) => {
            const thumbUrl = `https://img.youtube.com/vi/${vid}/hqdefault.jpg`;
            allCards.push({
                category: 'videos',
                html: `
                    <div class="card item-videos" onclick="playVideoIndex(${index})">
                        <div class="thumbnail" style="background-image: url('${thumbUrl}');">
                            <i class="fa-solid fa-play play-icon"></i>
                            <span class="badge" style="background:#ff0000;">SHORTS</span>
                        </div>
                        <div class="card-details">
                            <div class="avatar"><i class="fa-brands fa-youtube"></i></div>
                            <div class="info">
                                <h3>Featured Video #${index + 1}</h3>
                                <p>JoyMix Video Stream</p>
                            </div>
                        </div>
                    </div>`
            });
        });

        allCards.sort(() => 0.5 - Math.random());
        grid.innerHTML = allCards.map(c => c.html).join('');
    }

    function filterCategory(category, el) {
        document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
        el.classList.add('active');

        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.style.display = (category === 'all' || card.classList.contains('item-' + category)) ? 'flex' : 'none';
        });
    }

    function playDirectItem(path) {
        document.getElementById('nextBtn').style.display = 'none';
        document.getElementById('prevBtn').style.display = 'none';
        document.getElementById('mainFrame').src = path;
        document.getElementById('playerModal').style.display = 'flex';
    }

    function playVideoIndex(index) {
        if (index < 0 || index >= videoQueue.length) return;
        currentVideoIndex = index;
        document.getElementById('nextBtn').style.display = 'flex';
        document.getElementById('prevBtn').style.display = 'flex';
        const vidId = videoQueue[currentVideoIndex];
        document.getElementById('mainFrame').src = `https://www.youtube.com/embed/${vidId}?autoplay=1`;
        document.getElementById('playerModal').style.display = 'flex';
    }

    function nextVideo() {
        if (videoQueue.length === 0) return;
        currentVideoIndex = (currentVideoIndex + 1) % videoQueue.length;
        playVideoIndex(currentVideoIndex);
    }

    function prevVideo() {
        if (videoQueue.length === 0) return;
        currentVideoIndex = (currentVideoIndex - 1 + videoQueue.length) % videoQueue.length;
        playVideoIndex(currentVideoIndex);
    }

    function closePlayer() {
        document.getElementById('mainFrame').src = '';
        document.getElementById('playerModal').style.display = 'none';
    }

    // Auto load video feed dynamically after script injects
    loadFeed();
</script>"""

@app.route('/')
def home():
    return render_template_string(MAIN_HTML)

@app.route('/api/render-ui')
def render_ui():
    return BACKEND_UI_COMPONENT

if __name__ == '__main__':
    app.run(debug=True)
