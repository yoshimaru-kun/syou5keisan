import re

file_path = r"c:\Users\emyjy\OneDrive\デスクトップ\Antigravity\小5計算ゲーム\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. CSS
css_old = """        .choice-btn.wrong {
            background-color: #f44336;
            color: #fff;
            border-color: #f44336;
            box-shadow: 0 5px 0 #c62828;
        }"""
css_new = """        .choice-btn.wrong {
            background-color: #f44336;
            color: #fff;
            border-color: #f44336;
            box-shadow: 0 5px 0 #c62828;
        }

        .input-box {
            width: 100%;
            max-width: 250px;
            font-size: 2rem;
            padding: 10px;
            text-align: center;
            border: 3px solid var(--accent);
            border-radius: 15px;
            margin-bottom: 20px;
            color: var(--text);
        }

        .input-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }"""
html = html.replace(css_old, css_new)

# 2. Units array & vars
units_old = """        // データの定義
        const units = [
            { id: 1, name: "小数の計算", locked: false, icon: "🔢" },
            { id: 2, name: "体積", locked: true, icon: "📦" },
            { id: 3, name: "比例", locked: true, icon: "⚖️" },
            { id: 4, name: "分数の計算", locked: true, icon: "🍕" },
            { id: 5, name: "平均", locked: true, icon: "📊" },
            { id: 6, name: "単位量あたりの大きさ", locked: true, icon: "🚗" },
            { id: 7, name: "割合", locked: true, icon: "💯" },
        ];"""
units_new = """        // データの定義
        const units = [
            { id: 1, name: "小数の計算（ふつう・4択）", type: "choice", locked: false, icon: "🔢" },
            { id: 1, name: "小数の計算（ハード・入力）", type: "input", locked: false, icon: "🔥" },
            { id: 2, name: "体積", type: "choice", locked: true, icon: "📦" },
            { id: 3, name: "比例", type: "choice", locked: true, icon: "⚖️" },
            { id: 4, name: "分数の計算", type: "choice", locked: true, icon: "🍕" },
            { id: 5, name: "平均", type: "choice", locked: true, icon: "📊" },
            { id: 6, name: "単位量あたりの大きさ", type: "choice", locked: true, icon: "🚗" },
            { id: 7, name: "割合", type: "choice", locked: true, icon: "💯" },
        ];"""
html = html.replace(units_old, units_new)

# 3. State vars
vars_old = """        // 状態変数
        let currentUnitId = 1;
        let currentQuestionIndex = 0;"""
vars_new = """        // 状態変数
        let currentUnitId = 1;
        let currentQuizType = "choice";
        let currentQuestionIndex = 0;"""
html = html.replace(vars_old, vars_new)

# 4. renderUnits
render_old = """                if (!unit.locked) {
                    div.onclick = () => startQuiz(unit.id, unit.name);
                }"""
render_new = """                if (!unit.locked) {
                    div.onclick = () => startQuiz(unit.id, unit.name, unit.type);
                }"""
html = html.replace(render_old, render_new)

# 5. startQuiz definition
startq_old = """        function startQuiz(unitId, unitName) {
            currentUnitId = unitId;
            let allQuestions = quizData[unitId] || [];"""
startq_new = """        function startQuiz(unitId, unitName, quizType) {
            currentUnitId = unitId;
            currentQuizType = quizType;
            let allQuestions = quizData[unitId] || [];"""
html = html.replace(startq_old, startq_new)

# 6. showQuestion and checkAnswer
logic_old = """        // 問題の表示
        function showQuestion() {
            canAnswer = true;
            const q = currentQuestions[currentQuestionIndex];
            
            document.getElementById('question-progress').innerText = `${currentQuestionIndex + 1} / ${currentQuestions.length} 問`;
            document.getElementById('question-text').innerText = q.question;
            
            const choicesContainer = document.getElementById('choices-container');
            choicesContainer.innerHTML = '';

            // 解説や次へボタンを隠す
            document.getElementById('explanation-box').classList.remove('show');
            document.getElementById('next-btn').style.display = 'none';

            q.choices.forEach((choiceText, index) => {
                const btn = document.createElement('button');
                btn.className = 'choice-btn';
                btn.innerText = choiceText;
                btn.onclick = () => checkAnswer(index, btn);
                choicesContainer.appendChild(btn);
            });
        }

        // 答え合わせ
        function checkAnswer(selectedIndex, btnElement) {
            if (!canAnswer) return;
            canAnswer = false; // 連続タップ防止

            const q = currentQuestions[currentQuestionIndex];
            const isCorrect = (selectedIndex === q.correctIndex);
            
            showFeedback(isCorrect);

            const allBtns = document.querySelectorAll('.choice-btn');
            
            // 正解・不正解のスタイリング
            if (isCorrect) {
                btnElement.classList.add('correct');
                score += 20; // 1問20点で100点満点
            } else {
                btnElement.classList.add('wrong');
                // 正解のボタンも教える
                allBtns[q.correctIndex].classList.add('correct');
            }

            // 全ボタンを無効化
            allBtns.forEach(b => b.disabled = true);

            // 解説を表示
            document.getElementById('explanation-text').innerText = q.explanation;
            document.getElementById('explanation-box').classList.add('show');
            
            // 次へボタンを表示
            const nextBtn = document.getElementById('next-btn');
            if (currentQuestionIndex < currentQuestions.length - 1) {
                nextBtn.innerText = "つぎの問題へ ➡";
            } else {
                nextBtn.innerText = "結果を見る 🌟";
            }
            nextBtn.style.display = 'block';
        }"""

logic_new = """        // 問題の表示
        function showQuestion() {
            canAnswer = true;
            const q = currentQuestions[currentQuestionIndex];
            
            document.getElementById('question-progress').innerText = `${currentQuestionIndex + 1} / ${currentQuestions.length} 問`;
            document.getElementById('question-text').innerText = q.question;
            
            const choicesContainer = document.getElementById('choices-container');
            choicesContainer.innerHTML = '';

            // 解説や次へボタンを隠す
            document.getElementById('explanation-box').classList.remove('show');
            document.getElementById('next-btn').style.display = 'none';

            if (currentQuizType === 'choice') {
                choicesContainer.style.display = 'grid';
                q.choices.forEach((choiceText, index) => {
                    const btn = document.createElement('button');
                    btn.className = 'choice-btn';
                    btn.innerText = choiceText;
                    btn.onclick = () => checkAnswerChoice(index, btn);
                    choicesContainer.appendChild(btn);
                });
            } else {
                choicesContainer.style.display = 'flex';
                choicesContainer.innerHTML = `
                    <div class="input-container">
                        <input type="number" step="0.01" id="answer-input" class="input-box" placeholder="こたえは？">
                        <button class="btn" style="width:100%; max-width:250px;" id="submit-answer-btn" onclick="checkAnswerInput()">答える</button>
                    </div>
                `;
                setTimeout(() => {
                    const el = document.getElementById('answer-input');
                    if(el) {
                        el.focus();
                        // Enterキーでの回答送信機能を追加
                        el.addEventListener('keypress', function(e) {
                            if (e.key === 'Enter') checkAnswerInput();
                        });
                    }
                }, 100);
            }
        }

        // 答え合わせ (4択)
        function checkAnswerChoice(selectedIndex, btnElement) {
            handleAnswerResult(selectedIndex === currentQuestions[currentQuestionIndex].correctIndex, btnElement);
        }

        // 答え合わせ (入力)
        function checkAnswerInput() {
            const inputEl = document.getElementById('answer-input');
            const submitBtn = document.getElementById('submit-answer-btn');
            if (!inputEl.value) return; // 空なら何もしない
            
            const q = currentQuestions[currentQuestionIndex];
            const correctStr = String(q.choices[q.correctIndex]);
            
            // 値の比較
            const isCorrect = (Number(inputEl.value) === Number(correctStr));
            
            handleAnswerResult(isCorrect, null);
            inputEl.disabled = true;
            submitBtn.disabled = true;
            
            if (!isCorrect) {
                inputEl.style.backgroundColor = '#fce4e4';
                inputEl.type = 'text';
                inputEl.value = `❌ 君:${inputEl.value} / ⭕️ 正解:${correctStr}`;
                inputEl.style.fontSize = '1.0rem';
            } else {
                inputEl.style.backgroundColor = '#e8f5e9';
            }
        }

        // 答え合わせ共通処理
        function handleAnswerResult(isCorrect, btnElement) {
            if (!canAnswer) return;
            canAnswer = false;

            const q = currentQuestions[currentQuestionIndex];
            showFeedback(isCorrect);
            
            if (isCorrect) {
                if (btnElement) btnElement.classList.add('correct');
                score += 20;
            } else {
                if (btnElement) btnElement.classList.add('wrong');
                if (currentQuizType === 'choice') {
                    const allBtns = document.querySelectorAll('.choice-btn');
                    if(allBtns[q.correctIndex]) allBtns[q.correctIndex].classList.add('correct');
                }
            }

            if (currentQuizType === 'choice') {
                document.querySelectorAll('.choice-btn').forEach(b => b.disabled = true);
            }
ｋｌ
            document.getElementById('explanation-text').innerText = q.explanation;
            document.getElementById('explanation-box').classList.add('show');
            
            const nextBtn = document.getElementById('next-btn');
            if (currentQuestionIndex < currentQuestions.length - 1) {
                nextBtn.innerText = "つぎの問題へ ➡";
            } else {
                nextBtn.innerText = "結果を見る 🌟";
            }
            nextBtn.style.display = 'block';
        }"""
html = html.replace(logic_old, logic_new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Changes applied!")
