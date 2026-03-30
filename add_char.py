import sys

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. CSS
    css_target = "            .screen { padding: 20px; }\n        }\n    </style>"
    css_replacement = """            .screen { padding: 20px; }
        }

        /* キャラクター選択画面 */
        .characters-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            width: 100%;
            max-width: 400px;
            margin-bottom: 20px;
        }

        .char-card {
            background-color: var(--light);
            border: 3px solid var(--primary);
            border-radius: 15px;
            padding: 10px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .char-card.selected {
            background-color: #FFE0B2;
            border-color: #E65100;
            box-shadow: 0 0 10px #FF9800;
            transform: scale(1.05);
        }

        .char-card img {
            width: 100px;
            height: 100px;
            object-fit: contain;
            margin-bottom: 5px;
        }

        .char-name {
            font-size: 1rem;
            font-weight: 800;
        }

        /* ゲーム中のキャラクター表示 */
        .in-game-character {
            position: absolute;
            bottom: 20px;
            right: 20px;
            width: 80px;
            height: 80px;
            opacity: 0.9;
            transition: transform 0.3s;
            z-index: 5;
        }
        
        .in-game-character.jumping {
            animation: bounceIn 0.5s ease-in-out;
        }
        
        .result-character {
            width: 150px;
            height: 150px;
            margin: 10px auto;
            object-fit: contain;
            display: block;
        }
    </style>"""
    # handle crlf
    content = content.replace("            .screen { padding: 20px; }\r\n        }\r\n    </style>", css_replacement)
    content = content.replace(css_target, css_replacement)

    # 2. HTML: character screen
    html1_target = "<button class=\"btn start-btn\" onclick=\"showScreen('unit-screen')\">スタート！</button>\n        </div>\n\n        <!-- 単元選択画面 -->"
    html1_target_crlf = html1_target.replace('\n', '\r\n')
    
    html1_replacement = """<button class="btn start-btn" onclick="showScreen('character-screen')">スタート！</button>
        </div>

        <!-- キャラクター選択画面 -->
        <div id="character-screen" class="screen">
            <h2>いっしょにぼうけんする<br>なかまをえらんでね！</h2>
            <br>
            <div class="characters-grid" id="characters-container">
                <!-- JavaScriptで生成 -->
            </div>
            <button class="btn start-btn" id="char-decide-btn" disabled onclick="showScreen('unit-screen')">決定！</button>
            <button class="btn" style="background-color: #9E9E9E; box-shadow: 0 6px 0 #616161;" onclick="showScreen('title-screen')">もどる</button>
        </div>

        <!-- 単元選択画面 -->"""
    
    content = content.replace(html1_target, html1_replacement).replace(html1_target_crlf, html1_replacement)

    # 3. HTML: quiz screen char img
    html2_target = "<span id=\"question-progress\">1 / 5 問</span>\n            </div>\n            \n            <div class=\"question-box\""
    html2_target_crlf = html2_target.replace('\n', '\r\n')
    html2_replacement = """<span id="question-progress">1 / 5 問</span>
            </div>
            
            <img src="" id="quiz-character-img" class="in-game-character" style="display:none;" alt="character">
            
            <div class="question-box\""""
    
    content = content.replace(html2_target, html2_replacement).replace(html2_target_crlf, html2_replacement)

    # 4. HTML: result screen char img
    html3_target = "<span id=\"score-text\">0</span>点\n            </div>\n\n            <div class=\"result-msg\""
    html3_target_crlf = html3_target.replace('\n', '\r\n')
    html3_replacement = """<span id="score-text">0</span>点
            </div>

            <img src="" id="result-character-img" class="result-character" style="display:none;" alt="character">

            <div class="result-msg\""""
    content = content.replace(html3_target, html3_replacement).replace(html3_target_crlf, html3_replacement)

    # 5. JS init
    js1_target = "let canAnswer = true;\n        let currentQuestions = [];\n\n        // 初期化処理"
    js1_target_crlf = js1_target.replace('\n', '\r\n')
    js1_replacement = """let canAnswer = true;
        let currentQuestions = [];

        // キャラクターデータ
        const gameCharacters = [
            { id: 1, name: "ニンジャ", image: "images/char1.png" },
            { id: 2, name: "まほうつかい", image: "images/char2.png" },
            { id: 3, name: "お坊さん", image: "images/char3.png" },
            { id: 4, name: "ガンナー", image: "images/char4.png" }
        ];
        let currentSelectedCharacter = null;

        // 初期化処理"""
    content = content.replace(js1_target, js1_replacement).replace(js1_target_crlf, js1_replacement)
    
    js1b_target = "function initApp() {\n            renderUnits();\n        }"
    js1b_target_crlf = js1b_target.replace('\n', '\r\n')
    js1b_replacement = """function initApp() {
            renderUnits();
            renderCharacters();
        }

        // キャラクター選択描画
        function renderCharacters() {
            const container = document.getElementById('characters-container');
            container.innerHTML = '';
            gameCharacters.forEach(char => {
                const card = document.createElement('div');
                card.className = 'char-card';
                card.innerHTML = `
                    <img src="${char.image}" alt="${char.name}">
                    <div class="char-name">${char.name}</div>
                `;
                card.onclick = () => selectCharacter(char, card);
                container.appendChild(card);
            });
        }

        function selectCharacter(char, cardElement) {
            currentSelectedCharacter = char;
            
            // 選択状態のUI更新
            document.querySelectorAll('.char-card').forEach(c => c.classList.remove('selected'));
            cardElement.classList.add('selected');
            
            // 決定ボタン有効化
            const decideBtn = document.getElementById('char-decide-btn');
            if (decideBtn) decideBtn.disabled = false;
            
            // 各画面のキャラ画像も設定
            const quizImg = document.getElementById('quiz-character-img');
            const resultImg = document.getElementById('result-character-img');
            if (quizImg && resultImg) {
                quizImg.src = char.image;
                quizImg.style.display = 'block';
                resultImg.src = char.image;
                resultImg.style.display = 'block';
            }
        }"""
    content = content.replace(js1b_target, js1b_replacement).replace(js1b_target_crlf, js1b_replacement)

    # 6. JS checkAnswer (jumping)
    js2_target = "showFeedback(isCorrect);\n            \n            if (isCorrect) {"
    js2_target_crlf = js2_target.replace('\n', '\r\n')
    js2_replacement = """showFeedback(isCorrect);
            
            // キャラクターアニメーション
            const charImg = document.getElementById('quiz-character-img');
            if(charImg && currentSelectedCharacter) {
                charImg.classList.remove('jumping');
                void charImg.offsetWidth; // trigger reflow
                charImg.classList.add('jumping');
            }
            
            if (isCorrect) {"""
    content = content.replace(js2_target, js2_replacement).replace(js2_target_crlf, js2_replacement)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

process_file('index.html')
