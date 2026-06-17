# educational_games.py
# سیستم پیشرفته بازی‌های آموزشی - نسخه حرفه‌ای با 8 بازی مختلف

def render_games_page(session_id):
    return f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>بازی‌های آموزشی | مسیرینو</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: white;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(5deg); }}
        }}
        @keyframes bounce {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            75% {{ transform: translateX(5px); }}
        }}
        @keyframes confetti {{
            0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
            100% {{ transform: translateY(100vh) rotate(720deg); opacity: 0; }}
        }}
        
        .game-card {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}
        .game-card:hover {{
            transform: translateY(-10px) scale(1.02);
            background: rgba(108,99,255,0.2);
            border-color: rgba(108,99,255,0.5);
        }}
        
        .float-animation {{ animation: float 3s ease-in-out infinite; }}
        
        .modal-glass {{
            background: rgba(15, 12, 41, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .option-btn {{
            transition: all 0.2s ease;
            cursor: pointer;
        }}
        .option-btn:hover {{ transform: scale(1.02); }}
        .option-btn.correct {{
            background: linear-gradient(135deg, #10b981, #059669);
            animation: bounce 0.3s ease;
        }}
        .option-btn.wrong {{
            background: linear-gradient(135deg, #ef4444, #dc2626);
            animation: shake 0.3s ease;
        }}
        
        .confetti {{
            position: fixed;
            width: 10px;
            height: 10px;
            position: absolute;
            animation: confetti 3s ease-out forwards;
        }}
        
        @media (max-width: 768px) {{
            h1 {{ font-size: 1.8rem; }}
        }}
    </style>
</head>
<body class="relative">
    <div class="fixed top-4 right-4 left-4 z-50 flex justify-between items-center">
        <a href="/?session_id={session_id}" class="px-5 py-2 rounded-full bg-white/10 backdrop-blur-lg hover:bg-white/20 transition-all duration-300 flex items-center gap-2">
            <span>←</span> <span>بازگشت</span>
        </a>
        <div class="px-5 py-2 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 backdrop-blur-lg flex items-center gap-2">
            <span>🏆</span>
            <span id="totalScoreDisplay" class="font-bold">0</span>
            <span>امتیاز</span>
        </div>
    </div>

    <div class="container mx-auto px-4 py-24 max-w-7xl">
        <h1 class="text-5xl md:text-7xl font-bold text-center mb-4 bg-gradient-to-r from-white via-purple-400 to-pink-500 bg-clip-text text-transparent">
            🎮 بازی‌های آموزشی
        </h1>
        <p class="text-center text-gray-400 mb-12 text-lg">با بازی یاد بگیر، امتیاز جمع کن و بهترین شو!</p>
        
        <div id="gameSelectorPage">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" id="gamesGrid"></div>
        </div>
        
        <div id="gamePlayPage" style="display: none;">
            <div class="flex items-center gap-4 mb-6">
                <button onclick="backToGames()" class="px-4 py-2 rounded-full bg-white/10 hover:bg-white/20 transition">
                    ← بازگشت به بازی‌ها
                </button>
                <div class="flex-1"></div>
                <div class="px-4 py-2 rounded-full bg-purple-600/50">
                    <span id="gameScoreDisplay">0</span> امتیاز این بازی
                </div>
            </div>
            <div id="gameContent"></div>
        </div>
        
        <div id="resultModal" class="fixed inset-0 z-50 flex items-center justify-center hidden modal-glass" onclick="closeModal()">
            <div class="bg-gradient-to-br from-purple-900/90 to-pink-900/90 rounded-3xl p-8 max-w-md w-full mx-4 text-center border border-white/20" onclick="event.stopPropagation()">
                <div id="modalIcon" class="text-6xl mb-4">🎉</div>
                <h2 id="modalTitle" class="text-2xl font-bold mb-2">تبریک!</h2>
                <p id="modalMessage" class="text-gray-300 mb-4"></p>
                <div class="flex gap-3">
                    <button onclick="closeModal()" class="flex-1 py-3 rounded-full bg-white/20 hover:bg-white/30 transition">بستن</button>
                    <button onclick="playAgain()" class="flex-1 py-3 rounded-full bg-gradient-to-r from-purple-600 to-pink-500 hover:opacity-90 transition">بازی مجدد</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const sessionId = "{session_id}";
        let currentGameId = null;
        let totalScore = 0;
        let currentGameScore = 0;
        
        const GAMES = [
            {{ id: "quiz", name: "🎯 مسابقه هوشمند", icon: "🎯", description: "به سوالات تستی پاسخ بده و امتیاز بگیر", difficulty: "متوسط", color: "from-purple-500 to-pink-500" }},
            {{ id: "flashcard", name: "📇 فلش‌کارت‌های هوشمند", icon: "📇", description: "با فلش‌کارت‌ها درس بخون", difficulty: "آسان", color: "from-blue-500 to-cyan-500" }},
            {{ id: "memory", name: "🧠 بازی حافظه", icon: "🧠", description: "کارت‌های مرتبط رو پیدا کن", difficulty: "متوسط", color: "from-green-500 to-emerald-500" }},
            {{ id: "hangman", name: "🪢 دار و دسته", icon: "🪢", description: "کلمه رو با حدس زدن حروف پیدا کن", difficulty: "متوسط", color: "from-orange-500 to-red-500" }},
            {{ id: "math-challenge", name: "🔢 چالش ریاضی", icon: "🔢", description: "معادلات ریاضی رو حل کن", difficulty: "سخت", color: "from-yellow-500 to-orange-500" }},
            {{ id: "true-false", name: "✅❌ درست یا نادرست", icon: "❓", description: "به جملات علمی پاسخ بده", difficulty: "آسان", color: "from-teal-500 to-green-500" }},
            {{ id: "matching", name: "🔗 جورچین مفاهیم", icon: "🔗", description: "اصطلاحات رو با تعریفشون جور کن", difficulty: "سخت", color: "from-indigo-500 to-purple-500" }},
            {{ id: "speed-quiz", name: "⚡ مسابقه سریع", icon: "⚡", description: "تا میتونی سریع جواب بده", difficulty: "سخت", color: "from-red-500 to-pink-500" }}
        ];
        
        const QUIZ_QUESTIONS = [
            {{ q: "قانون اول نیوتن چیست؟", options: ["قانون لختی", "F=ma", "عکس‌العمل", "جاذبه"], correct: 0 }},
            {{ q: "فرمول مساحت دایره", options: ["πr²", "2πr", "πd", "r²"], correct: 0 }},
            {{ q: "واحد نیرو در سیستم SI", options: ["نیوتن", "ژول", "وات", "پاسکال"], correct: 0 }},
            {{ q: "سرعت نور در خلاء چند کیلومتر بر ثانیه است؟", options: ["300,000", "150,000", "3,000", "30,000"], correct: 0 }},
            {{ q: "کدام یک جزء سلول گیاهی نیست؟", options: ["دیواره سلولی", "کلروپلاست", "سانتریول", "واکوئل"], correct: 2 }},
            {{ q: "قانون اهم چه رابطه‌ای را بیان می‌کند؟", options: ["V=IR", "P=VI", "I=V/R", "هر دو V=IR و I=V/R"], correct: 3 }},
            {{ q: "نماد شیمیایی طلا چیست؟", options: ["Go", "Au", "Ag", "Fe"], correct: 1 }},
            {{ q: "میانگین سرعت چگونه محاسبه می‌شود؟", options: ["مسافت/زمان", "زمان/مسافت", "شتاب/زمان", "نیرو/جرم"], correct: 0 }}
        ];
        
        const TRUE_FALSE_QUESTIONS = [
            {{ statement: "زمین به دور خورشید می‌چرخد", isTrue: true }},
            {{ statement: "آب در دمای 100 درجه سانتی‌گراد یخ می‌زند", isTrue: false }},
            {{ statement: "نور سریع‌ترین پدیده در جهان است", isTrue: true }},
            {{ statement: "انسان 2 ریه دارد", isTrue: true }},
            {{ statement: "خورشید یک سیاره است", isTrue: false }},
            {{ statement: "مغز انسان حدود 2% وزن بدن را تشکیل می‌دهد", isTrue: true }}
        ];
        
        const MATCHING_PAIRS = [
            {{ term: "DNA", definition: "ماده ژنتیکی" }},
            {{ term: "میتوکندری", definition: "نیروگاه سلول" }},
            {{ term: "ریبوزوم", definition: "ساخت پروتئین" }},
            {{ term: "کلروپلاست", definition: "محل فتوسنتز" }},
            {{ term: "هسته", definition: "مرکز فرماندهی سلول" }},
            {{ term: "غشا سلولی", definition: "محافظ و ورود و خروج مواد" }}
        ];
        
        const MATH_QUESTIONS = [
            {{ q: "12 + 23 = ?", answer: 35, options: [32, 33, 34, 35] }},
            {{ q: "45 - 18 = ?", answer: 27, options: [25, 26, 27, 28] }},
            {{ q: "7 × 8 = ?", answer: 56, options: [48, 54, 56, 64] }},
            {{ q: "81 ÷ 9 = ?", answer: 9, options: [7, 8, 9, 10] }},
            {{ q: "25% از 200 = ?", answer: 50, options: [25, 40, 50, 60] }}
        ];
        
        const FLASHCARDS = [
            {{ q: "قانون اول نیوتن", a: "هر جسمی در حالت سکون یا حرکت یکنواخت می‌ماند مگر نیرویی به آن وارد شود" }},
            {{ q: "نظریه سلول", a: "همه موجودات زنده از سلول تشکیل شده‌اند" }},
            {{ q: "قانون پایستگی انرژی", a: "انرژی نه ایجاد می‌شود و نه از بین می‌رود" }},
            {{ q: "DNA چیست؟", a: "ماده ژنتیکی که اطلاعات وراثتی را منتقل می‌کند" }},
            {{ q: "فتوسنتز", a: "فرآیند ساخت غذا توسط گیاهان با کمک نور خورشید" }}
        ];
        
        const HANGMAN_WORDS = ["پایتون", "ریاضی", "فیزیک", "شیمی", "زیست", "ادبیات", "تاریخ", "جغرافیا"];
        
        function renderGamesGrid() {{
            let html = '';
            for (let i = 0; i < GAMES.length; i++) {{
                const g = GAMES[i];
                html += '<div class="game-card rounded-2xl p-6 cursor-pointer" onclick="startGame(\\'' + g.id + '\\')">' +
                    '<div class="text-6xl mb-4 float-animation">' + g.icon + '</div>' +
                    '<h3 class="text-xl font-bold mb-2">' + g.name + '</h3>' +
                    '<p class="text-gray-400 text-sm mb-3">' + g.description + '</p>' +
                    '<div class="flex justify-between items-center">' +
                        '<span class="px-3 py-1 rounded-full text-xs bg-white/10">' + g.difficulty + '</span>' +
                        '<span class="text-purple-400">شروع کن →</span>' +
                    '</div>' +
                '</div>';
            }}
            document.getElementById('gamesGrid').innerHTML = html;
        }}
        
        function startGame(gameId) {{
            currentGameId = gameId;
            currentGameScore = 0;
            document.getElementById('gameScoreDisplay').innerText = currentGameScore;
            document.getElementById('gameSelectorPage').style.display = 'none';
            document.getElementById('gamePlayPage').style.display = 'block';
            
            if (gameId === 'quiz') startQuizGame();
            else if (gameId === 'flashcard') startFlashcardGame();
            else if (gameId === 'memory') startMemoryGame();
            else if (gameId === 'hangman') startHangmanGame();
            else if (gameId === 'math-challenge') startMathChallenge();
            else if (gameId === 'true-false') startTrueFalseGame();
            else if (gameId === 'matching') startMatchingGame();
            else if (gameId === 'speed-quiz') startSpeedQuiz();
        }}
        
        function startQuizGame() {{
            let qIndex = 0;
            let score = 0;
            let locked = false;
            const questions = [...QUIZ_QUESTIONS];
            
            function render() {{
                if (qIndex >= questions.length) {{
                    finishGame(score, questions.length, "🎉 مسابقه تمام شد!");
                    return;
                }}
                const q = questions[qIndex];
                let optionsHtml = '';
                for (let i = 0; i < q.options.length; i++) {{
                    optionsHtml += '<div class="option-btn bg-white/10 rounded-xl p-3 mb-2 text-center" onclick="answerQuiz(' + i + ')">' + q.options[i] + '</div>';
                }}
                document.getElementById('gameContent').innerHTML = 
                    '<div class="bg-gradient-to-br from-purple-900/30 to-pink-900/30 rounded-3xl p-6 md:p-8">' +
                        '<div class="flex justify-between items-center mb-6">' +
                            '<span class="px-4 py-2 rounded-full bg-white/10">سوال ' + (qIndex+1) + '/' + questions.length + '</span>' +
                            '<span class="px-4 py-2 rounded-full bg-yellow-500/30">⭐ ' + score + ' امتیاز</span>' +
                        '</div>' +
                        '<div class="text-xl md:text-2xl font-bold mb-8 text-center">' + q.q + '</div>' +
                        '<div id="quizOptions">' + optionsHtml + '</div>' +
                        '<div id="explanation" class="mt-4 text-center text-gray-400 text-sm"></div>' +
                    '</div>';
                window.currentQuizAnswer = q.correct;
                locked = false;
            }}
            
            window.answerQuiz = function(selected) {{
                if (locked) return;
                const isCorrect = (selected === window.currentQuizAnswer);
                if (isCorrect) {{
                    score += 10;
                    currentGameScore += 10;
                    document.getElementById('gameScoreDisplay').innerText = currentGameScore;
                    showConfetti();
                }}
                const options = document.querySelectorAll('.option-btn');
                for (let idx = 0; idx < options.length; idx++) {{
                    if (idx === window.currentQuizAnswer) options[idx].classList.add('correct');
                    if (idx === selected && !isCorrect) options[idx].classList.add('wrong');
                }}
                const explanation = document.getElementById('explanation');
                explanation.innerHTML = isCorrect ? '✅ صحیح! +10 امتیاز' : '❌ نادرست!';
                locked = true;
                setTimeout(function() {{ qIndex++; render(); }}, 1500);
            }};
            
            render();
        }}
        
        function startFlashcardGame() {{
            let index = 0;
            let showAnswer = false;
            let score = 0;
            const cards = FLASHCARDS;
            
            function render() {{
                const card = cards[index];
                document.getElementById('gameContent').innerHTML = 
                    '<div class="bg-gradient-to-br from-blue-900/30 to-cyan-900/30 rounded-3xl p-8">' +
                        '<div class="flex justify-between items-center mb-6">' +
                            '<span>فلش‌کارت ' + (index+1) + '/' + cards.length + '</span>' +
                            '<span>⭐ ' + score + ' امتیاز</span>' +
                        '</div>' +
                        '<div class="rounded-2xl p-12 text-center cursor-pointer min-h-[250px] flex items-center justify-center bg-gradient-to-r from-purple-600 to-pink-600" onclick="toggleAnswer()">' +
                            '<div class="text-xl md:text-2xl font-bold">' + (showAnswer ? card.a : card.q) + '</div>' +
                        '</div>' +
                        '<div class="flex gap-4 mt-6">' +
                            '<button class="flex-1 py-3 rounded-full bg-white/20" onclick="prevCard()">◀ قبلی</button>' +
                            '<button class="flex-1 py-3 rounded-full bg-green-600" onclick="markKnown()">✓ بلدم (+5)</button>' +
                            '<button class="flex-1 py-3 rounded-full bg-white/20" onclick="nextCard()">بعدی ▶</button>' +
                        '</div>' +
                        '<p class="text-center text-gray-400 text-sm mt-4">(روی کارت کلیک کن تا پاسخ ببینی)</p>' +
                    '</div>';
            }}
            
            window.toggleAnswer = function() {{ showAnswer = !showAnswer; render(); }};
            window.prevCard = function() {{ if (index > 0) {{ index--; showAnswer = false; render(); }} }};
            window.nextCard = function() {{ if (index < cards.length - 1) {{ index++; showAnswer = false; render(); }} else {{ finishGame(score, cards.length, "🎓 تبریک! فلش‌کارت‌ها تموم شد!"); }} }};
            window.markKnown = function() {{ score += 5; currentGameScore += 5; document.getElementById('gameScoreDisplay').innerText = currentGameScore; showConfetti(); nextCard(); }};
            render();
        }}
        
        function startMemoryGame() {{
            const pairs = [
                {{ id: 1, text: "HTML", match: "زبان ساختار وب" }},
                {{ id: 2, text: "CSS", match: "زبان طراحی وب" }},
                {{ id: 3, text: "JavaScript", match: "زبان برنامه‌نویسی وب" }},
                {{ id: 4, text: "Python", match: "زبان برنامه‌نویسی قدرتمند" }}
            ];
            let cards = [];
            for (let p of pairs) {{
                cards.push({{ id: Math.random(), text: p.text, pairId: p.id, type: 'term' }});
                cards.push({{ id: Math.random(), text: p.match, pairId: p.id, type: 'def' }});
            }}
            cards = cards.sort(function() {{ return Math.random() - 0.5; }});
            let selected = null;
            let matched = [];
            let locked = false;
            let score = 0;
            
            function render() {{
                let html = '<div class="grid grid-cols-2 md:grid-cols-4 gap-3">';
                for (let i = 0; i < cards.length; i++) {{
                    const c = cards[i];
                    const isMatched = matched.includes(c.id);
                    const isSelected = (selected === i);
                    let bgStyle = '';
                    if (isMatched) bgStyle = 'opacity:0.4';
                    if (isSelected) bgStyle = 'background:#6c63ff';
                    html += '<div class="bg-white/10 rounded-xl p-4 text-center cursor-pointer transition hover:bg-purple-600/50 min-h-[80px] flex items-center justify-center" onclick="selectCard(' + i + ')" style="' + bgStyle + '">' +
                        (isMatched ? '✓' : (isSelected ? c.text : '❓')) +
                    '</div>';
                }}
                html += '</div><div class="mt-4 text-center">امتیاز: ' + score + '</div>';
                document.getElementById('gameContent').innerHTML = html;
            }}
            
            window.selectCard = function(idx) {{
                if (locked || matched.includes(cards[idx].id)) return;
                if (selected === null) {{ selected = idx; render(); }}
                else {{
                    const first = cards[selected];
                    const second = cards[idx];
                    if (first.pairId === second.pairId && first.type !== second.type) {{
                        matched.push(first.id, second.id);
                        score += 10;
                        currentGameScore += 10;
                        document.getElementById('gameScoreDisplay').innerText = currentGameScore;
                        selected = null;
                        render();
                        if (matched.length === cards.length) finishGame(score, pairs.length * 2, "🎉 حافظه‌ات عالیه!");
                        showConfetti();
                    }} else {{
                        locked = true;
                        render();
                        setTimeout(function() {{ selected = null; locked = false; render(); }}, 800);
                    }}
                }}
            }};
            render();
        }}
        
        function startHangmanGame() {{
            let word = HANGMAN_WORDS[Math.floor(Math.random() * HANGMAN_WORDS.length)];
            let guessed = new Array(word.length).fill('_');
            let attempts = 6;
            let guessedLetters = [];
            let score = 0;
            
            function render() {{
                let hangmanStates = ['⚪', '😮', '😅', '😰', '😱', '💀', '☠️'];
                let letters = 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'.split('');
                let buttonsHtml = '';
                for (let i = 0; i < letters.length; i++) {{
                    let l = letters[i];
                    let isDisabled = guessedLetters.includes(l);
                    buttonsHtml += '<button class="px-3 py-2 bg-white/10 rounded-lg hover:bg-purple-600 transition" onclick="guessLetter(\\'' + l + '\\')" ' + (isDisabled ? 'disabled' : '') + '>' + l + '</button>';
                }}
                document.getElementById('gameContent').innerHTML = 
                    '<div class="bg-gradient-to-br from-orange-900/30 to-red-900/30 rounded-3xl p-6 md:p-8 text-center">' +
                        '<div class="text-6xl mb-4">' + hangmanStates[6-attempts] + '</div>' +
                        '<div class="text-3xl font-mono mb-6 tracking-wider">' + guessed.join(' ') + '</div>' +
                        '<div class="mb-4">تعداد حدس‌های باقی‌مانده: ' + attempts + '</div>' +
                        '<div class="mb-4 text-gray-400">حروف حدس زده شده: ' + (guessedLetters.join(', ') || '-') + '</div>' +
                        '<div class="grid grid-cols-5 gap-2 mb-6">' + buttonsHtml + '</div>' +
                    '</div>';
            }}
            
            window.guessLetter = function(letter) {{
                if (guessedLetters.includes(letter) || attempts <= 0) return;
                guessedLetters.push(letter);
                if (word.includes(letter)) {{
                    for (let i = 0; i < word.length; i++) {{
                        if (word[i] === letter) guessed[i] = letter;
                    }}
                    if (!guessed.includes('_')) {{
                        score += (attempts * 5);
                        currentGameScore += score;
                        finishGame(score, 30, "🎉 کلمه رو پیدا کردی! +" + score + " امتیاز");
                        return;
                    }}
                }} else {{
                    attempts--;
                    if (attempts === 0) {{
                        finishGame(0, 30, "😢 بازی تمام شد! کلمه: " + word);
                        return;
                    }}
                }}
                render();
            }};
            render();
        }}
        
        function startMathChallenge() {{
            let qIndex = 0;
            let score = 0;
            let timeLeft = 15;
            let timer;
            const questions = [...MATH_QUESTIONS];
            
            function startTimer() {{
                if (timer) clearInterval(timer);
                timeLeft = 15;
                timer = setInterval(function() {{
                    timeLeft--;
                    const timerEl = document.getElementById('timer');
                    if (timerEl) timerEl.innerText = timeLeft;
                    if (timeLeft <= 0) {{
                        clearInterval(timer);
                        nextQuestion();
                    }}
                }}, 1000);
            }}
            
            function nextQuestion() {{
                qIndex++;
                if (qIndex >= questions.length) finishGame(score, questions.length, "🎉 چالش ریاضی تموم شد!");
                else render();
            }}
            
            function render() {{
                if (timer) clearInterval(timer);
                const q = questions[qIndex];
                let optionsHtml = '';
                for (let i = 0; i < q.options.length; i++) {{
                    optionsHtml += '<div class="option-btn bg-white/10 rounded-xl p-3 mb-2 text-center" onclick="checkAnswer(' + q.options[i] + ')">' + q.options[i] + '</div>';
                }}
                document.getElementById('gameContent').innerHTML = 
                    '<div class="bg-gradient-to-br from-yellow-900/30 to-orange-900/30 rounded-3xl p-6 md:p-8">' +
                        '<div class="flex justify-between items-center mb-6">' +
                            '<span>سوال ' + (qIndex+1) + '/' + questions.length + '</span>' +
                            '<span>⭐ ' + score + ' امتیاز</span>' +
                            '<span id="timer" class="px-4 py-2 rounded-full bg-red-500/50">' + timeLeft + '</span>' +
                        '</div>' +
                        '<div class="text-2xl md:text-3xl font-bold text-center mb-8">' + q.q + '</div>' +
                        '<div id="options">' + optionsHtml + '</div>' +
                    '</div>';
                startTimer();
            }}
            
            window.checkAnswer = function(answer) {{
                clearInterval(timer);
                if (answer === questions[qIndex].answer) {{
                    score += timeLeft;
                    currentGameScore += timeLeft;
                    document.getElementById('gameScoreDisplay').innerText = currentGameScore;
                    showConfetti();
                }}
                nextQuestion();
            }};
            render();
        }}
        
        function startTrueFalseGame() {{
            let qIndex = 0;
            let score = 0;
            const questions = [...TRUE_FALSE_QUESTIONS];
            
            function render() {{
                if (qIndex >= questions.length) {{
                    finishGame(score, questions.length, "🎉 عالی! همه رو جواب دادی!");
                    return;
                }}
                const q = questions[qIndex];
                document.getElementById('gameContent').innerHTML = 
                    '<div class="bg-gradient-to-br from-teal-900/30 to-green-900/30 rounded-3xl p-6 md:p-8 text-center">' +
                        '<div class="mb-6">سوال ' + (qIndex+1) + '/' + questions.length + ' | ⭐ ' + score + ' امتیاز</div>' +
                        '<div class="text-xl md:text-2xl font-bold mb-8">' + q.statement + '</div>' +
                        '<div class="flex gap-4">' +
                            '<button class="flex-1 py-4 rounded-full bg-green-600 text-xl" onclick="answer(true)">✅ درست</button>' +
                            '<button class="flex-1 py-4 rounded-full bg-red-600 text-xl" onclick="answer(false)">❌ نادرست</button>' +
                        '</div>' +
                        '<div id="tfExplanation" class="mt-4 text-gray-400"></div>' +
                    '</div>';
            }}
            
            window.answer = function(isTrue) {{
                const q = questions[qIndex];
                const isCorrect = (isTrue === q.isTrue);
                if (isCorrect) {{
                    score += 10;
                    currentGameScore += 10;
                    document.getElementById('gameScoreDisplay').innerText = currentGameScore;
                    showConfetti();
                }}
                document.getElementById('tfExplanation').innerHTML = isCorrect ? '✅ صحیح!' : '❌ نادرست!';
                setTimeout(function() {{ qIndex++; render(); }}, 1500);
            }};
            render();
        }}
        
        function startMatchingGame() {{
            let terms = [...MATCHING_PAIRS];
            let selectedTerm = null;
            let matched = [];
            let score = 0;
            
            function shuffle(array) {{
                for (let i = array.length - 1; i > 0; i--) {{
                    const j = Math.floor(Math.random() * (i + 1));
                    [array[i], array[j]] = [array[j], array[i]];
                }}
                return array;
            }}
            
            let shuffledTerms = shuffle([...terms]);
            let shuffledDefs = shuffle([...terms]);
            
            function render() {{
                let html = '<div class="grid grid-cols-1 md:grid-cols-2 gap-6"><div><h3 class="text-center mb-4">📖 اصطلاحات</h3>';
                for (let i = 0; i < shuffledTerms.length; i++) {{
                    const t = shuffledTerms[i];
                    const isMatched = matched.includes(t.term);
                    let bgStyle = '';
                    if (isMatched) bgStyle = 'opacity:0.4';
                    if (selectedTerm === i) bgStyle = 'background:#6c63ff';
                    html += '<div class="option-btn bg-white/10 rounded-xl p-3 mb-2 text-center" onclick="selectTerm(' + i + ')" style="' + bgStyle + '">' + t.term + '</div>';
                }}
                html += '</div><div><h3 class="text-center mb-4">📝 تعاریف</h3>';
                for (let i = 0; i < shuffledDefs.length; i++) {{
                    const d = shuffledDefs[i];
                    const isMatched = matched.includes(d.definition);
                    let bgStyle = isMatched ? 'opacity:0.4' : '';
                    html += '<div class="option-btn bg-white/10 rounded-xl p-3 mb-2 text-center" onclick="selectDef(' + i + ')" style="' + bgStyle + '">' + d.definition + '</div>';
                }}
                html += '</div></div><div class="mt-4 text-center">امتیاز: ' + score + '</div>';
                document.getElementById('gameContent').innerHTML = html;
            }}
            
            window.selectTerm = function(idx) {{
                if (matched.includes(shuffledTerms[idx].term)) return;
                selectedTerm = idx;
                render();
            }};
            
            window.selectDef = function(idx) {{
                if (selectedTerm === null) return;
                const term = shuffledTerms[selectedTerm];
                const def = shuffledDefs[idx];
                if (term.definition === def.definition && !matched.includes(term.term)) {{
                    matched.push(term.term, def.definition);
                    score += 10;
                    currentGameScore += 10;
                    document.getElementById('gameScoreDisplay').innerText = currentGameScore;
                    showConfetti();
                    selectedTerm = null;
                    render();
                    if (matched.length === terms.length * 2) finishGame(score, terms.length, "🎉 همه رو درست جور کردی!");
                }} else {{
                    selectedTerm = null;
                    render();
                }}
            }};
            render();
        }}
        
        function startSpeedQuiz() {{
            let questions = [...QUIZ_QUESTIONS];
            let qIndex = 0;
            let score = 0;
            let startTime = Date.now();
            let timeLimit = 30;
            let timer;
            
            function startTimer() {{
                if (timer) clearInterval(timer);
                timer = setInterval(function() {{
                    const elapsed = Math.floor((Date.now() - startTime) / 1000);
                    const remaining = timeLimit - elapsed;
                    const timerEl = document.getElementById('speedTimer');
                    if (timerEl) timerEl.innerText = remaining;
                    if (remaining <= 0) {{
                        clearInterval(timer);
                        finishGame(score, questions.length, "⏰ زمان تمام شد!");
                    }}
                }}, 100);
            }}
            
            function render() {{
                if (qIndex >= questions.length) {{
                    finishGame(score, questions.length, "🎉 عالی! همه سوالات رو جواب دادی!");
                    return;
                }}
                const q = questions[qIndex];
                let optionsHtml = '';
                for (let i = 0; i < q.options.length; i++) {{
                    optionsHtml += '<div class="option-btn bg-white/10 rounded-xl p-3 mb-2 text-center" onclick="speedAnswer(' + i + ')">' + q.options[i] + '</div>';
                }}
                document.getElementById('gameContent').innerHTML = 
                    '<div class="bg-gradient-to-br from-red-900/30 to-pink-900/30 rounded-3xl p-6 md:p-8">' +
                        '<div class="flex justify-between items-center mb-6">' +
                            '<span>سوال ' + (qIndex+1) + '/' + questions.length + '</span>' +
                            '<span>⭐ ' + score + ' امتیاز</span>' +
                            '<span id="speedTimer" class="px-4 py-2 rounded-full bg-yellow-500/50">' + timeLimit + '</span>' +
                        '</div>' +
                        '<div class="text-xl md:text-2xl font-bold text-center mb-8">' + q.q + '</div>' +
                        '<div id="speedOptions">' + optionsHtml + '</div>' +
                    '</div>';
            }}
            
            window.speedAnswer = function(selected) {{
                const isCorrect = (selected === questions[qIndex].correct);
                if (isCorrect) {{
                    const timeBonus = Math.max(0, timeLimit - Math.floor((Date.now() - startTime) / 1000));
                    score += 5 + timeBonus;
                    currentGameScore += 5 + timeBonus;
                    document.getElementById('gameScoreDisplay').innerText = currentGameScore;
                    showConfetti();
                }}
                qIndex++;
                startTime = Date.now();
                render();
            }};
            
            startTimer();
            render();
        }}
        
        function showConfetti() {{
            for (let i = 0; i < 30; i++) {{
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + '%';
                confetti.style.top = '50%';
                confetti.style.backgroundColor = ['#ffd700', '#ff6584', '#6c63ff', '#10b981'][Math.floor(Math.random() * 4)];
                confetti.style.width = (Math.random() * 10 + 5) + 'px';
                confetti.style.height = confetti.style.width;
                document.body.appendChild(confetti);
                setTimeout(function() {{ confetti.remove(); }}, 3000);
            }}
        }}
        
        function finishGame(score, total, message) {{
            totalScore += currentGameScore;
            localStorage.setItem('gameTotalScore_' + sessionId, totalScore);
            document.getElementById('totalScoreDisplay').innerText = totalScore;
            document.getElementById('modalIcon').innerHTML = score >= total*0.7 ? '🏆' : '🎮';
            document.getElementById('modalTitle').innerText = score >= total*0.7 ? 'تبریک!' : 'بازی تمام شد';
            document.getElementById('modalMessage').innerHTML = message + '<br>امتیاز شما: ' + score + ' از ' + (total*10);
            document.getElementById('resultModal').classList.remove('hidden');
        }}
        
        function playAgain() {{
            closeModal();
            startGame(currentGameId);
        }}
        
        function closeModal() {{
            document.getElementById('resultModal').classList.add('hidden');
            backToGames();
        }}
        
        function backToGames() {{
            currentGameId = null;
            document.getElementById('gameSelectorPage').style.display = 'block';
            document.getElementById('gamePlayPage').style.display = 'none';
            document.getElementById('gameContent').innerHTML = '';
        }}
        
        // راه‌اندازی اولیه
        renderGamesGrid();
        totalScore = parseInt(localStorage.getItem('gameTotalScore_' + sessionId) || '0');
        document.getElementById('totalScoreDisplay').innerText = totalScore;
    </script>
</body>
</html>'''