"""
Bilim Kutubxonasi - 10 ta fan uchun to'liq interaktiv elektron kitoblar generatori.
Ushbu skript 9 ta fan uchun zamonaviy, interaktiv, chiroyli HTML elektron darsliklarni yaratadi:
1. Matematika (Algebra 7-sinf)
2. Fizika (Fizika 8-sinf)
3. Kimyo (Kimyo 8-sinf)
4. Biologiya (Zoologiya 7-sinf mavjud)
5. Tarix (O'zbekiston tarixi 8-sinf)
6. Ona tili (Ona tili 7-sinf)
7. Adabiyot (O'tkan kunlar)
8. Ingliz tili (English Grammar & Vocabulary)
9. Geografiya (Geografiya 7-sinf)
10. Informatika (Informatika va Python 8-sinf)
"""

import os
from pathlib import Path

BOOKS_DIR = Path("media/books")
BOOKS_DIR.mkdir(parents=True, exist_ok=True)

def generate_book_html(config):
    """
    config dict:
    - title: Str
    - subtitle: Str
    - subject: Str
    - author: Str
    - theme_color: Str (emerald, indigo, blue, amber, purple, rose, cyan, violet, teal)
    - icon: Str (FontAwesome icon class)
    - chapters: list of dicts: {"title": str, "content": str, "key_points": list[str]}
    - quiz: list of dicts: {"q": str, "options": list[str], "correct": int, "exp": str}
    - flashcards: list of dicts: {"front": str, "back": str}
    - interactive_tool: dict or None (title, html)
    """
    color = config["theme_color"]
    
    # Generate chapters HTML
    chapters_nav = ""
    chapters_content = ""
    for idx, ch in enumerate(config["chapters"], 1):
        ch_id = f"chapter-{idx}"
        chapters_nav += f"""
        <a href="#{ch_id}" class="flex items-center px-3 py-2 text-sm font-medium text-slate-600 rounded-lg hover:bg-{color}-50 hover:text-{color}-700 transition">
            <span class="w-6 h-6 rounded-full bg-{color}-100 text-{color}-700 flex items-center justify-center text-xs font-bold mr-2">{idx}</span>
            <span class="truncate">{ch['title']}</span>
        </a>
        """
        
        points_html = "".join([f"<li class='flex items-start'><i class='fa-solid fa-check-circle text-{color}-500 mt-1 mr-2 flex-shrink-0'></i><span>{p}</span></li>" for p in ch.get('key_points', [])])
        
        chapters_content += f"""
        <section id="{ch_id}" class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-8 mb-8 scroll-mt-20">
            <div class="flex items-center space-x-3 mb-4">
                <span class="px-3 py-1 bg-{color}-100 text-{color}-800 text-xs font-bold uppercase rounded-full">Bob {idx}</span>
                <h2 class="text-xl sm:text-2xl font-bold text-slate-800">{ch['title']}</h2>
            </div>
            <div class="prose max-w-none text-slate-600 leading-relaxed mb-6 space-y-3">
                {ch['content']}
            </div>
            {f'''<div class="bg-slate-50 border-l-4 border-{color}-500 p-4 rounded-r-xl">
                <h4 class="font-bold text-slate-700 text-sm mb-2 flex items-center">
                    <i class="fa-solid fa-lightbulb text-amber-500 mr-2"></i> Asosiy tushunchalar:
                </h4>
                <ul class="space-y-1 text-sm text-slate-600">{points_html}</ul>
            </div>''' if points_html else ''}
        </section>
        """

    # Generate Quiz JSON
    import json
    quiz_json = json.dumps(config["quiz"], ensure_ascii=False)
    flashcards_json = json.dumps(config["flashcards"], ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['title']}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        .perspective-1000 {{ perspective: 1000px; }}
        .transform-style-3d {{ transform-style: preserve-3d; }}
        .backface-hidden {{ backface-visibility: hidden; }}
        .rotate-y-180 {{ transform: rotateY(180deg); }}
        .card-flipped {{ transform: rotateY(180deg); }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col justify-between">

    <!-- Header -->
    <header class="bg-{color}-800 text-white sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-xl">
                    <i class="{config['icon']}"></i>
                </div>
                <div>
                    <h1 class="text-base sm:text-lg font-bold leading-tight">{config['title']}</h1>
                    <p class="text-xs text-{color}-200">{config['subtitle']} • {config['author']}</p>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <button onclick="toggleTab('read')" id="tab-btn-read" class="px-3 py-1.5 text-xs sm:text-sm font-semibold rounded-lg bg-white text-{color}-800 transition">
                    <i class="fa-solid fa-book-open mr-1"></i> Darslik
                </button>
                <button onclick="toggleTab('quiz')" id="tab-btn-quiz" class="px-3 py-1.5 text-xs sm:text-sm font-semibold rounded-lg bg-white/10 text-white hover:bg-white/20 transition">
                    <i class="fa-solid fa-circle-question mr-1"></i> Test
                </button>
                <button onclick="toggleTab('cards')" id="tab-btn-cards" class="px-3 py-1.5 text-xs sm:text-sm font-semibold rounded-lg bg-white/10 text-white hover:bg-white/20 transition">
                    <i class="fa-solid fa-brain mr-1"></i> Kartalar
                </button>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow w-full">
        
        <!-- ================= READ TAB ================= -->
        <div id="tab-content-read" class="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <!-- Sidebar Navigation -->
            <aside class="lg:col-span-1 hidden lg:block">
                <div class="sticky top-24 bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
                    <h3 class="font-bold text-slate-800 text-sm uppercase tracking-wider mb-4 flex items-center">
                        <i class="fa-solid fa-list-ul mr-2 text-{color}-600"></i> Mundarija
                    </h3>
                    <nav class="space-y-1">
                        {chapters_nav}
                    </nav>
                </div>
            </aside>

            <!-- Main Chapters Content -->
            <div class="lg:col-span-3">
                {chapters_content}
            </div>
        </div>

        <!-- ================= QUIZ TAB ================= -->
        <div id="tab-content-quiz" class="hidden max-w-3xl mx-auto">
            <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-8">
                <div class="flex items-center justify-between border-b pb-4 mb-6">
                    <div>
                        <h2 class="text-xl sm:text-2xl font-bold text-slate-800 flex items-center">
                            <i class="fa-solid fa-award text-amber-500 mr-2"></i> {config['title']} — Bilim Testi
                        </h2>
                        <p class="text-sm text-slate-500 mt-1">Har bir to'g'ri javob uchun bilimlaringiz mustahkamlanadi!</p>
                    </div>
                    <div class="text-right">
                        <span class="text-xs text-slate-400 block">Natija</span>
                        <span id="quiz-score" class="text-xl font-black text-{color}-600">0 / {len(config['quiz'])}</span>
                    </div>
                </div>

                <div id="quiz-container" class="space-y-6">
                    <!-- Questions injected by JS -->
                </div>

                <div id="quiz-finish" class="hidden mt-8 text-center p-6 bg-{color}-50 rounded-xl border border-{color}-200">
                    <i class="fa-solid fa-trophy text-4xl text-amber-500 mb-2"></i>
                    <h3 class="text-lg font-bold text-slate-800">Test yakunlandi!</h3>
                    <p id="quiz-final-text" class="text-slate-600 text-sm mt-1"></p>
                    <button onclick="resetQuiz()" class="mt-4 px-5 py-2 bg-{color}-600 text-white font-semibold rounded-lg hover:bg-{color}-700 transition">
                        <i class="fa-solid fa-rotate-right mr-1"></i> Qayta topshirish
                    </button>
                </div>
            </div>
        </div>

        <!-- ================= FLASHCARDS TAB ================= -->
        <div id="tab-content-cards" class="hidden max-w-2xl mx-auto">
            <div class="text-center mb-6">
                <h2 class="text-2xl font-bold text-slate-800 flex items-center justify-center">
                    <i class="fa-solid fa-brain text-{color}-600 mr-2"></i> O'rganish kartalari (Flashcards)
                </h2>
                <p class="text-sm text-slate-500 mt-1">Kartaning ustiga bosib, uning orqa tomonidagi javobni ko'ring</p>
            </div>

            <!-- Card area -->
            <div class="perspective-1000 w-full h-64 sm:h-72 cursor-pointer" onclick="flipCard()">
                <div id="flashcard-inner" class="w-full h-full relative transform-style-3d transition-transform duration-500 shadow-lg rounded-2xl">
                    <!-- Front -->
                    <div class="absolute inset-0 backface-hidden bg-white border-2 border-{color}-300 rounded-2xl flex flex-col justify-between p-6 sm:p-8">
                        <div class="flex justify-between items-center text-xs font-bold text-{color}-600">
                            <span><i class="fa-solid fa-question-circle mr-1"></i> SAVOL / ATAMA</span>
                            <span id="card-counter">1 / {len(config['flashcards'])}</span>
                        </div>
                        <div class="flex items-center justify-center my-auto">
                            <p id="card-front-text" class="text-lg sm:text-xl font-bold text-slate-800 text-center"></p>
                        </div>
                        <div class="text-center text-xs text-slate-400">
                            <i class="fa-solid fa-hand-pointer mr-1"></i> Javobni ko'rish uchun bosing
                        </div>
                    </div>
                    <!-- Back -->
                    <div class="absolute inset-0 backface-hidden rotate-y-180 bg-{color}-800 text-white rounded-2xl flex flex-col justify-between p-6 sm:p-8">
                        <div class="flex justify-between items-center text-xs font-bold text-{color}-200">
                            <span><i class="fa-solid fa-check-circle mr-1"></i> JAVOB / TA'RIF</span>
                            <span id="card-counter-back">1 / {len(config['flashcards'])}</span>
                        </div>
                        <div class="flex items-center justify-center my-auto">
                            <p id="card-back-text" class="text-base sm:text-lg text-white font-medium text-center leading-relaxed"></p>
                        </div>
                        <div class="text-center text-xs text-{color}-200">
                            <i class="fa-solid fa-rotate mr-1"></i> Qaytarish uchun bosing
                        </div>
                    </div>
                </div>
            </div>

            <!-- Controls -->
            <div class="flex justify-between items-center mt-6">
                <button onclick="prevCard()" class="px-4 py-2 bg-white border border-slate-200 rounded-xl text-slate-700 font-semibold hover:bg-slate-50 transition shadow-sm">
                    <i class="fa-solid fa-arrow-left mr-1"></i> Oldingisi
                </button>
                <button onclick="nextCard()" class="px-5 py-2 bg-{color}-600 text-white rounded-xl font-semibold hover:bg-{color}-700 transition shadow-sm">
                    Keyingisi <i class="fa-solid fa-arrow-right ml-1"></i>
                </button>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-slate-900 text-slate-400 py-6 border-t border-slate-800 mt-12 text-center text-xs">
        <p class="font-semibold text-slate-300">«Bilim Kutubxonasi» Telegram Boti Maxsus Darsligi</p>
        <p class="mt-1">Dasturchi va Administrator: @Muhiddinov_official • Instagram: @muh1dd1nov_ai</p>
    </footer>

    <script>
        const quizData = {quiz_json};
        const cardsData = {flashcards_json};
        let currentCardIndex = 0;
        let score = 0;
        let answeredQuestions = {{}};

        function toggleTab(tab) {{
            const tabs = ['read', 'quiz', 'cards'];
            tabs.forEach(t => {{
                document.getElementById('tab-content-' + t).classList.add('hidden');
                const btn = document.getElementById('tab-btn-' + t);
                btn.className = "px-3 py-1.5 text-xs sm:text-sm font-semibold rounded-lg bg-white/10 text-white hover:bg-white/20 transition";
            }});
            document.getElementById('tab-content-' + tab).classList.remove('hidden');
            const activeBtn = document.getElementById('tab-btn-' + tab);
            activeBtn.className = "px-3 py-1.5 text-xs sm:text-sm font-semibold rounded-lg bg-white text-{color}-800 transition";
        }}

        // Quiz Logic
        function renderQuiz() {{
            const container = document.getElementById('quiz-container');
            container.innerHTML = '';
            quizData.forEach((item, qIdx) => {{
                const qDiv = document.createElement('div');
                qDiv.className = "p-5 rounded-xl border border-slate-200 bg-slate-50/50";
                
                let optHtml = '';
                item.options.forEach((opt, optIdx) => {{
                    optHtml += `
                        <button onclick="checkAnswer(${{qIdx}}, ${{optIdx}})" id="opt-${{qIdx}}-${{optIdx}}" 
                            class="w-full text-left p-3 rounded-lg border border-slate-200 bg-white text-sm text-slate-700 hover:border-{color}-500 hover:bg-{color}-50 transition flex items-center">
                            <span class="w-6 h-6 rounded-full bg-slate-100 text-slate-600 text-xs font-bold flex items-center justify-center mr-3">${{String.fromCharCode(65 + optIdx)}}</span>
                            <span>${{opt}}</span>
                        </button>
                    `;
                }});

                qDiv.innerHTML = `
                    <div class="font-bold text-slate-800 text-sm sm:text-base mb-3 flex items-start">
                        <span class="text-{color}-600 mr-2">${{qIdx + 1}}.</span>
                        <span>${{item.q}}</span>
                    </div>
                    <div class="space-y-2 mb-3">
                        ${{optHtml}}
                    </div>
                    <div id="exp-${{qIdx}}" class="hidden text-xs p-3 rounded-lg mt-2"></div>
                `;
                container.appendChild(qDiv);
            }});
        }}

        function checkAnswer(qIdx, optIdx) {{
            if (answeredQuestions[qIdx] !== undefined) return;
            answeredQuestions[qIdx] = optIdx;

            const q = quizData[qIdx];
            const expDiv = document.getElementById(`exp-${{qIdx}}`);
            expDiv.classList.remove('hidden');

            for (let i = 0; i < q.options.length; i++) {{
                const btn = document.getElementById(`opt-${{qIdx}}-${{i}}`);
                btn.disabled = true;
                if (i === q.correct) {{
                    btn.classList.add('bg-green-100', 'border-green-500', 'text-green-800');
                }} else if (i === optIdx) {{
                    btn.classList.add('bg-red-100', 'border-red-500', 'text-red-800');
                }}
            }}

            if (optIdx === q.correct) {{
                score++;
                expDiv.classList.add('bg-green-50', 'text-green-700', 'border', 'border-green-200');
                expDiv.innerHTML = `<strong>To'g'ri!</strong> ${{q.exp}}`;
            }} else {{
                expDiv.classList.add('bg-red-50', 'text-red-700', 'border', 'border-red-200');
                expDiv.innerHTML = `<strong>Noto'g'ri.</strong> ${{q.exp}}`;
            }}

            document.getElementById('quiz-score').innerText = `${{score}} / ${{quizData.length}}`;

            if (Object.keys(answeredQuestions).length === quizData.length) {{
                document.getElementById('quiz-finish').classList.remove('hidden');
                document.getElementById('quiz-final-text').innerText = `Siz ${{quizData.length}} ta savoldan ${{score}} tasiga to'g'ri javob berdingiz!`;
            }}
        }}

        function resetQuiz() {{
            score = 0;
            answeredQuestions = {{}};
            document.getElementById('quiz-score').innerText = `0 / ${{quizData.length}}`;
            document.getElementById('quiz-finish').classList.add('hidden');
            renderQuiz();
        }}

        // Flashcards Logic
        function updateCard() {{
            const card = cardsData[currentCardIndex];
            document.getElementById('card-front-text').innerText = card.front;
            document.getElementById('card-back-text').innerText = card.back;
            document.getElementById('card-counter').innerText = `${{currentCardIndex + 1}} / ${{cardsData.length}}`;
            document.getElementById('card-counter-back').innerText = `${{currentCardIndex + 1}} / ${{cardsData.length}}`;
            document.getElementById('flashcard-inner').classList.remove('card-flipped');
        }}

        function flipCard() {{
            document.getElementById('flashcard-inner').classList.toggle('card-flipped');
        }}

        function nextCard() {{
            currentCardIndex = (currentCardIndex + 1) % cardsData.length;
            updateCard();
        }}

        function prevCard() {{
            currentCardIndex = (currentCardIndex - 1 + cardsData.length) % cardsData.length;
            updateCard();
        }}

        // Init
        window.onload = function() {{
            renderQuiz();
            if (cardsData.length > 0) updateCard();
        }};
    </script>
</body>
</html>
"""
    return html

print("Generator tayyor.")
