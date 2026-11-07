import os
from pathlib import Path
from build_books import generate_book_html, BOOKS_DIR

books_data = [
    # 1. Matematika
    {
        "filename": "Algebra_7_sinf.html",
        "title": "Algebra 7-sinf",
        "subtitle": "Umumiy o'rta ta'lim maktablari uchun interaktiv darslik",
        "subject": "Matematika",
        "author": "Sh. Alimov, A. Xolmuhamedov",
        "theme_color": "blue",
        "icon": "fa-solid fa-calculator",
        "chapters": [
            {
                "title": "1-bob. Algebraik ifodalar va birhadlar",
                "content": "<p>Sonli va harfli ifodalar matematikaning asosiy tili hisoblanadi. Harflar bilan belgilangan ifodalarda o'zgaruvchilar qatnashadi. Birhad deb faqat sonlar, o'zgaruvchilar va ularning darajalarining ko'paytmasidan iborat bo'lgan ifodaga aytiladi.</p><p>Masalan: <b>5x</b>, <b>-3a²b</b>, <b>12x³y⁴</b> — bular birhadlardir. Birhadning standart shaklida faqat bitta sonli ko'paytuvchi (koeffitsiyent) birinchi o'rinda yoziladi.</p>",
                "key_points": [
                    "Birhadning darajasi — o'zgaruvchilar daraja ko'rsatkichlarining yig'indisi.",
                    "O'xshash birhadlar — harfiy qismi bir xil bo'lgan birhadlar.",
                    "Birhadlarni ko'paytirishda bir xil asosli darajalar qo'shiladi: aᵐ · aⁿ = aᵐ⁺ⁿ"
                ]
            },
            {
                "title": "2-bob. Ko'phadlar va ular ustida amallar",
                "content": "<p>Bir nechta birhadlarning algebraik yig'indisi <b>ko'phad</b> deyiladi. Ko'phadni standart shaklga keltirish uchun undagi o'xshash birhadlar ixchamlanadi.</p><p>Ko'phadlarni qo'shish va ayirishda qavslarni ochish qoidalariga rioya qilinadi: agar qavs oldida minus ishorasi bo'lsa, qavs ichidagi barcha ishoralar qarama-qarshisiga o'zgaradi.</p>",
                "key_points": [
                    "Ko'phadning darajasi — uning tarkibidagi eng katta darajali birhadning darajasi.",
                    "Ko'phadni birhadga ko'paytirish: a(b + c) = ab + ac (taqsimot qonuni).",
                    "Ko'phadlarni guruhlash usuli bilan ko'paytuvchilarga ajratish."
                ]
            },
            {
                "title": "3-bob. Qisqa ko'paytirish formulalari",
                "content": "<p>Algebraik hisoblashlarni tez va oson bajarish uchun qisqa ko'paytirish formulalari juda muhim vositadir:</p><div class='bg-blue-50 p-4 rounded-xl font-mono text-sm space-y-1 my-3 text-blue-900'><div>1. (a + b)² = a² + 2ab + b² (Yig'indining kvadrati)</div><div>2. (a - b)² = a² - 2ab + b² (Ayirmaning kvadrati)</div><div>3. a² - b² = (a - b)(a + b) (Kvadratlar ayirmasi)</div><div>4. (a + b)³ = a³ + 3a²b + 3ab² + b³</div><div>5. a³ + b³ = (a + b)(a² - ab + b²)</div></div>",
                "key_points": [
                    "Kvadratlar ayirmasi formulasi har doim ko'paytuvchilarga ajratishda ishlatiladi.",
                    "Qisqa ko'paytirish formulalari og'zaki hisoblashda ham qulaylik beradi."
                ]
            },
            {
                "title": "4-bob. Bir noma'lumli chiziqli tenglamalar",
                "content": "<p><b>ax = b</b> ko'rinishidagi tenglamaga bir noma'lumli chiziqli tenglama deyiladi (bunda a ≠ 0). Agar a ≠ 0 bo'lsa, tenglama yagona x = b/a ildizga ega.</p><p>Tenglamaning asosiy xossasi: tenglamaning har ikkala tomoniga bir xil sonni qo'shish, ayirish, yoki 0 dan farqli songa ko'paytirish/bo'lish mumkin.</p>",
                "key_points": [
                    "Noma'lum qatnashgan hadlar chap tomonga, ma'lum sonlar o'ng tomonga o'tkaziladi.",
                    "Had boshqa tomonga o'tganda ishorasi qarama-qarshisiga o'zgaradi."
                ]
            }
        ],
        "quiz": [
            {"q": "Qisqa ko'paytirish formulasi: (a - b)² nimaga teng?", "options": ["a² - b²", "a² - 2ab + b²", "a² + 2ab + b²", "a² - 2ab - b²"], "correct": 1, "exp": "(a - b)² = a² - 2ab + b² (ayirmaning kvadrati formulasi)."},
            {"q": "2x + 10 = 24 tenglamaning ildizini toping:", "options": ["x = 5", "x = 7", "x = 12", "x = 14"], "correct": 1, "exp": "2x = 24 - 10 => 2x = 14 => x = 7."},
            {"q": "x² - 16 ifodani ko'paytuvchilarga ajrating:", "options": ["(x - 4)²", "(x - 4)(x + 4)", "(x - 8)(x + 2)", "(x - 16)(x + 1)"], "correct": 1, "exp": "a² - b² = (a - b)(a + b) formulasi bo'yicha: x² - 4² = (x - 4)(x + 4)."},
            {"q": "3a² · 4a³ ko'paytmasini toping:", "options": ["12a⁵", "7a⁵", "12a⁶", "7a⁶"], "correct": 0, "exp": "Koeffitsiyentlar ko'payadi (3*4=12), bir xil asosli darajalar qo'shiladi (2+3=5): 12a⁵."}
        ],
        "flashcards": [
            {"front": "Kvadratlar ayirmasi formulasi qanday?", "back": "a² - b² = (a - b)(a + b)"},
            {"front": "Birhad nima?", "back": "Faqat sonlar, o'zgaruvchilar va ularning butun darajalaridan iborat ko'paytma."},
            {"front": "Chiziqli tenglama umumiy ko'rinishi qanday?", "back": "ax = b (a ≠ 0 bo'lganda yagona yechim x = b/a bo'ladi)"}
        ]
    },

    # 2. Fizika
    {
        "filename": "Fizika_8_sinf.html",
        "title": "Fizika 8-sinf",
        "subtitle": "Issiqlik va elektr hodisalari bo'yicha interaktiv qo'llanma",
        "subject": "Fizika",
        "author": "P. Habibullayev, A. Boydedayev",
        "theme_color": "amber",
        "icon": "fa-solid fa-bolt",
        "chapters": [
            {
                "title": "1-bob. Issiqlik harakati va ichki energiya",
                "content": "<p>Jismni tashkil qilgan molekula va atomlarning betartib harakati <b>issiqlik harakati</b> deyiladi. Harorat — molekulalar o'rtacha kinetik energiyasining o'lchovidir.</p><p>Jismning barcha zarrachalari harakatining kinetik energiyasi va o'zaro ta'sir potensial energiyasining yig'indisi jismning <b>ichki energiyasi</b> deyiladi. Ichki energiyani mexanik ish bajarish yoki issiqlik uzatish orqali o'zgartirish mumkin.</p>",
                "key_points": [
                    "Issiqlik miqdori formulasi: Q = c · m · (t₂ - t₁)",
                    "c — moddaning solishtirma issiqlik sig'imi (J/(kg·°C)).",
                    "Issiqlik uzatish turlari: issiqlik o'tkazuvchanlik, konveksiya va nurlanish."
                ]
            },
            {
                "title": "2-bob. Elektr toki va Om qonuni",
                "content": "<p>Zaryadlangan zarrachalarning tartibli (yo'naltirilgan) harakati <b>elektr toki</b> deb ataladi. Metallarda elektr tokini erkin elektronlar tashiydi.</p><p><b>Zanjir qismi uchun Om qonuni:</b> Zanjir qismidagi tok kuchi (I) shu qismdagi kuchlanishga (U) to'g'ri mutanosib va uning qarshiligiga (R) teskari mutanosibdir:</p><div class='bg-amber-50 p-4 rounded-xl font-mono text-center text-lg font-bold text-amber-900 my-3'>I = U / R</div>",
                "key_points": [
                    "Tok kuchi (I) — Amper (A), Ampermetr zanjirga ketma-ket ulanadi.",
                    "Kuchlanish (U) — Volt (V), Voltmetr zanjirga parallel ulanadi.",
                    "Elektr qarshiligi (R) — Om (Ω), R = ρ · (l / S)."
                ]
            },
            {
                "title": "3-bob. Elektr tokining ishi va quvvati. Joul-Lens qonuni",
                "content": "<p>Elektr maydoni zaryadlarni ko'chirishda ish bajaradi: <b>A = U · I · t</b>. Elektr tokining quvvati birlik vaqt ichida bajarilgan ishga teng: <b>P = A / t = U · I</b> (Vatt).</p><p><b>Joul-Lens qonuni:</b> Tokli o'tkazgichdan ajralib chiqadigan issiqlik miqdori tok kuchining kvadrati, o'tkazgich qarshiligi va tok o'tish vaqtining ko'paytmasiga teng: <b>Q = I² · R · t</b>.</p>",
                "key_points": [
                    "O'tkazgichlar ketma-ket ulanganda: I = const, R_umumiy = R₁ + R₂.",
                    "O'tkazgichlar parallel ulanganda: U = const, 1/R_umumiy = 1/R₁ + 1/R₂."
                ]
            }
        ],
        "quiz": [
            {"q": "Zanjir qismi uchun Om qonuni formulasi qaysi?", "options": ["I = U · R", "I = U / R", "U = I / R", "R = I / U"], "correct": 1, "exp": "Om qonuniga ko'ra tok kuchi: I = U / R."},
            {"q": "Kuchlanish qaysi asbob yordamida o'lchanadi va u qanday ulanadi?", "options": ["Ampermetr, ketma-ket", "Voltmetr, parallel", "Voltmetr, ketma-ket", "Reostat, parallel"], "correct": 1, "exp": "Kuchlanish voltmetr bilan o'lchanadi va u zanjir qismiga parallel ulanadi."},
            {"q": "Joul-Lens qonuni formulasini ko'rsating:", "options": ["Q = c · m · Δt", "Q = I² · R · t", "A = F · s", "E = m · c²"], "correct": 1, "exp": "Joul-Lens qonuni: Q = I² · R · t."},
            {"q": "100 Om qarshilikka ega o'tkazgichga 220 V kuchlanish berilsa, tok kuchi qancha bo'ladi?", "options": ["22 000 A", "2.2 A", "0.45 A", "22 A"], "correct": 1, "exp": "I = U / R = 220 / 100 = 2.2 A."}
        ],
        "flashcards": [
            {"front": "Om qonuni qanday ta'riflanadi?", "back": "Zanjir qismidagi tok kuchi kuchlanishga to'g'ri, qarshilikka teskari mutanosib: I = U / R"},
            {"front": "Elektr toki nima?", "back": "Zaryadlangan zarrachalarning yo'naltirilgan tartibli harakati."},
            {"front": "Tok quvvatining o'lchov birligi nima?", "back": "Vatt (Vt). 1 Vt = 1 V · 1 A."}
        ]
    },

    # 3. Kimyo
    {
        "filename": "Kimyo_8_sinf.html",
        "title": "Kimyo 8-sinf",
        "subtitle": "Anorganik kimyo va davriy qonun asoslari",
        "subject": "Kimyo",
        "author": "I. Asqarov, N. To'xtayev",
        "theme_color": "purple",
        "icon": "fa-solid fa-flask-vial",
        "chapters": [
            {
                "title": "1-bob. D.I. Mendeleyevning davriy qonuni va jadvali",
                "content": "<p>1869-yilda D.I. Mendeleyev buyuk kashfiyot — davriy qonunni yaratdi. Oddiy moddalar va ularning birikmalari shakl hamda xossalari elementlarning atom massalariga (zamonaviy tushunchada atom yadrosi zaryadiga) davriy ravishda bog'liqdir.</p><p>Davriy jadvalda gorizontal qatorlar <b>davrlar</b> (7 ta), vertikal ustunlar esa <b>guruhlar</b> (8 ta asosiy va qo'shimcha guruhchalar) deyiladi.</p>",
                "key_points": [
                    "Tartib raqami (Z) = Yadrodagi protonlar soni = Elektronlar soni.",
                    "Davr raqami = Atomdagi elektron qavatlar soni.",
                    "Guruh raqami (asosiy guruhcha) = Tashqi qavatdagi valent elektronlar soni."
                ]
            },
            {
                "title": "2-bob. Kimyoviy bog'lanish turlari",
                "content": "<p>Atomlar barqaror 8 elektronli tashqi qavat (oktet qoidasi) hosil qilish uchun o'zaro birikadi. Kimyoviy bog'lanishning 4 asosiy turi mavjud:</p><ul class='list-disc pl-5 space-y-1 my-2'><li><b>Kovalent qutbsiz:</b> Bir xil metallmaslar o'rtasida (H₂, O₂, Cl₂).</li><li><b>Kovalent qutbli:</b> Har xil metallmaslar o'rtasida umumiy elektron juft hisobiga (HCl, H₂O, NH₃).</li><li><b>Ion bog'lanish:</b> Metall va metallmas atomlari o'rtasida elektron o'tishi natijasida (NaCl, CaO).</li><li><b>Metall bog'lanish:</b> Metall ionlari va erkin elektronlar («elektron gaz») o'rtasida.</li></ul>",
                "key_points": [
                    "Elektrmanfiylik — atomning umumiy elektron juftni o'ziga tortish xususiyati.",
                    "Eng elektrmanfiy element — Ftor (F)."
                ]
            },
            {
                "title": "3-bob. Anorganik birikmalarning asosiy sinflari",
                "content": "<p>Anorganik moddalar 4 ta asosiy sinfga bo'linadi: <b>Oksidlar</b> (element + kislorod, masalan: CO₂, Na₂O), <b>Asoslar</b> (metall + OH guruhi, masalan: NaOH, Ca(OH)₂), <b>Kislotalar</b> (vodorod + kislota qoldig'i, masalan: HCl, H₂SO₄), va <b>Tuzlar</b> (metall + kislota qoldig'i, masalan: NaCl, CuSO₄).</p>",
                "key_points": [
                    "Neytrallanish reaksiyasi: Kislota + Asos = Tuz + Suv (HCl + NaOH = NaCl + H₂O).",
                    "Lakmus kislotada qizaradi, ishqorda ko'karadi."
                ]
            }
        ],
        "quiz": [
            {"q": "Atom yadrosi qanday zarrachalardan iborat?", "options": ["Faqat protonlar", "Proton va elektronlar", "Proton va neytronlar", "Elektron va pozitronlar"], "correct": 2, "exp": "Atom yadrosi musbat zaryadli protonlar va neytral neytronlardan iborat."},
            {"q": "NaCl (osh tuzi) molekulasida bog'lanishning qaysi turi mavjud?", "options": ["Kovalent qutbsiz", "Ion bog'lanish", "Vodorod bog'lanish", "Metall bog'lanish"], "correct": 1, "exp": "Metall (Na) va metallmas (Cl) o'rtasida ion bog'lanish hosil bo'ladi."},
            {"q": "Eng yuqori elektrmanfiylikka ega bo'lgan kimyoviy element qaysi?", "options": ["Kislorod (O)", "Xlor (Cl)", "Ftor (F)", "Kaliy (K)"], "correct": 2, "exp": "Davriy jadvalda eng yuqori elektrmanfiylik Ftor (F) elementiga xos (4.0)."},
            {"q": "Neytrallanish reaksiyasi natijasida nimalar hosil bo'ladi?", "options": ["Oksid va vodorod", "Tuz va suv", "Asos va kislota", "Faqat tuz"], "correct": 1, "exp": "Kislota va asos reaksiyaga kirishganda tuz va suv hosil bo'ladi."}
        ],
        "flashcards": [
            {"front": "D.I. Mendeleyev jadvalida davr nimani bildiradi?", "back": "Gorizontal qator bo'lib, atomdagi elektron qavatlar sonini ko'rsatadi."},
            {"front": "Ion bog'lanish qanday hosil bo'ladi?", "back": "Metall va metallmas o'rtasida elektronning to'liq ko'chib o'tishi va qarama-qarshi ionlar tortishuvi hisobiga."},
            {"front": "Kislota qoldig'i nima?", "back": "Kislota molekulasidagi vodorod atomlaridan tashqari qolgan atomlar guruhi."}
        ]
    },

    # 4. Tarix
    {
        "filename": "Ozbekiston_Tarixi_8_sinf.html",
        "title": "O'zbekiston Tarixi 8-sinf",
        "subtitle": "XVI asrdan XIX asr o'rtalarigacha bo'lgan davr",
        "subject": "Tarix",
        "author": "A. Muhammadjonov",
        "theme_color": "rose",
        "icon": "fa-solid fa-landmark",
        "chapters": [
            {
                "title": "1-bob. Shayboniylar davlati davri (XVI asr)",
                "content": "<p>1500-1501-yillarda Shayboniyxon boshchiligidagi ko'chmanchi o'zbeklar Temuriylar davlatidagi o'zaro nizolardan foydalanib Movarounnahrni egalladi. Poytaxt dastlab Samarqand, keyinchalik Buxoroga ko'chirildi.</p><p>Shayboniylar davrida Buxoro madaniy va diniy markazga aylandi. Abdullaxon II davrida (1583-1598) butun Movarounnahr va Xuroson yagona markazlashgan davlatga birlashtirildi, ko'plab karvonsaroylar, sardobalar va madrasalar bunyod etildi.</p>",
                "key_points": [
                    "Buxorodagi mashhur Ko'kaldosh madrasasi va Mir Arab madrasasi Shayboniylar davrida qurilgan.",
                    "1598-yilda Abdullaxon II vafotidan so'ng sulola inqirozga yuz tutdi."
                ]
            },
            {
                "title": "2-bob. Uch xonlik davri: Buxoro, Xiva va Qo'qon",
                "content": "<p>XVIII asrga kelib O'zbekiston hududida uchta mustaqil davlat shakllandi: <b>Buxoro amirligi</b> (Mang'itlar sulolasi), <b>Xiva xonligi</b> (Qo'ng'irotlar sulolasi) va <b>Qo'qon xonligi</b> (Minglar sulolasi).</p><p>Ushbu davlatlar o'zaro urushlar, tashqi savdo yo'llari va hududlar uchun kurash olib bordi. Shunga qaramay, Xivadagi Ichan Qal'a me'moriy ansambli, Qo'qondagi Xudoyorxon o'rdasi kabi nodir yodgorliklar qad rostladi.</p>",
                "key_points": [
                    "1756-yilda Muhammad Rahimiy Mang'itlar sulolasiga asos soldi va amir unvonini oldi.",
                    "Qo'qon xonligida Nodirabegim, Uvaysiy va Fazliy kabi ijodkorlar homiylik ko'rdi."
                ]
            }
        ],
        "quiz": [
            {"q": "Shayboniylar davlatida butun Movarounnahrni yagona markazga birlashtirgan hukmdor kim?", "options": ["Shayboniyxon", "Ubaydullaxon", "Abdullaxon II", "Abdulmo'minxon"], "correct": 2, "exp": "Abdullaxon II (1583-1598) barcha tarqoq viloyatlarni markaziy hokimiyatga bo'ysundirdi."},
            {"q": "Buxoro amirligida qaysi sulola hukmronlik qilgan?", "options": ["Shayboniylar", "Ashtarxoniylar", "Mang'itlar", "Qo'ng'irotlar"], "correct": 2, "exp": "1756-yildan 1920-yilgacha Buxoro amirligida Mang'itlar sulolasi hukmronlik qildi."},
            {"q": "Qo'qon xonligida Minglar sulolasiga kim asos solgan?", "options": ["Shohruhbiy", "Madalixon", "Xudoyorxon", "Olimxon"], "correct": 0, "exp": "1709-yilda Shohruhbiy mustaqil Qo'qon xonligiga asos soldi."},
            {"q": "Xivadagi jahon durdonasi hisoblangan tarixiy shahar qismi nima deb ataladi?", "options": ["Dishan Qal'a", "Ichan Qal'a", "Ark", "Registon"], "correct": 1, "exp": "Ichan Qal'a — Xivaning devor bilan o'ralgan qadimiy ichki shahar qismi bo'lib, YUNESKO merosiga kiritilgan."}
        ],
        "flashcards": [
            {"front": "O'zbekistonda uch xonlik qaysilar bo'lgan?", "back": "Buxoro amirligi, Xiva xonligi va Qo'qon xonligi."},
            {"front": "Buxoroda amirlik tuzumi qachon boshlangan?", "back": "1756-yilda Muhammad Rahimiy Mang'itlar sulolasini taxtga o'tkazishi bilan."},
            {"front": "Mir Arab madrasasi qaysi davrda bunyod etilgan?", "back": "XVI asrda Shayboniylar hukmronligi davrida (Ubaydullaxon zamonida)."}
        ]
    },

    # 5. Ona tili
    {
        "filename": "Ona_Tili_7_sinf.html",
        "title": "Ona Tili 7-sinf",
        "subtitle": "Morfologiya, fe'l shakllari va imlo qoidalari",
        "subject": "Ona tili",
        "author": "N. Mahmudov, A. Sobirov",
        "theme_color": "teal",
        "icon": "fa-solid fa-pen-nib",
        "chapters": [
            {
                "title": "1-bob. Fe'l so'z turkumi va uning tuzilishi",
                "content": "<p>Harakat yoki holatni bildirib, nima qildi? nima qilyapti? nima qiladi? kabi so'roqlarga javob bo'ladigan mustaqil so'z turkumi <b>fe'l</b> deyiladi. Fe'llar tuzilishiga ko'ra: sodda (o'qidi), qo'shma (sotib oldi), juft (aytdi-qo'ydi) va takroriy (yura-yura) bo'ladi.</p>",
                "key_points": [
                    "Fe'l zamonlari: o'tgan zamon (-di, -gan), hozirgi zamon (-yap, -moqda), kelasi zamon (-moqchi, -ajak, -r).",
                    "Bo'lishli va bo'lishsiz fe'llar (-ma qo'shimchasi yoki 'emas' so'zi bilan)."
                ]
            },
            {
                "title": "2-bob. Fe'l nisbatlari",
                "content": "<p>Harakat bilan uning bajaruvchisi o'rtasidagi munosabatni ifodalovchi shakllar <b>fe'l nisbatlari</b> deyiladi. O'zbek tilida 5 ta fe'l nisbati bor:</p><div class='space-y-1 my-2 text-sm bg-teal-50 p-4 rounded-xl text-teal-900'><div>1. <b>Aniq nisbat:</b> maxsus qo'shimchasi yo'q (yozdi, o'qidi).</div><div>2. <b>O'zlik nisbati:</b> -in, -il, -ish (yuvindi, kiyindi).</div><div>3. <b>Majhul nisbat:</b> -il, -in (xat yozildi, yer haydaldi).</div><div>4. <b>Birgalik nisbati:</b> -ish, -sh (kulishdi, gaplashdilar).</div><div>5. <b>Orttirma nisbati:</b> -dir, -tir, -t, -ir, -sat (yozdirdi, o'qitdi).</div></div>",
                "key_points": [
                    "Majhul nisbatda harakat egasi aniq aytilmaydi yoki grammatik to'ldiruvchi bo'lib keladi.",
                    "Orttirma nisbatda harakat boshqa shaxsga qildirildi."
                ]
            },
            {
                "title": "3-bob. Fe'lning vazifadosh shakllari",
                "content": "<p>Fe'lning asosiy ma'nosini saqlab, boshqa so'z turkumlari vazifasida keladigan shakllari <b>vazifadosh shakllar</b> deyiladi: <b>Sifatdosh</b> (-gan, -yotgan, -ar), <b>Ravishdosh</b> (-b, -ib, -gach, -guncha, -may), va <b>Harakat nomi</b> (-ish, -moq, -uv).</p>",
                "key_points": [
                    "Sifatdosh otga bog'lanib, uning belgisini bildiradi: 'kelgan mehmon'.",
                    "Ravishdosh fe'lga bog'lanib, harakatning tarzini bildiradi: 'kulib gapirdi'."
                ]
            }
        ],
        "quiz": [
            {"q": "'Xat kecha kotib tomonidan yozildi' jumlasidagi fe'l qaysi nisbatda?", "options": ["Aniq nisbat", "O'zlik nisbati", "Majhul nisbat", "Orttirma nisbat"], "correct": 2, "exp": "'Yozildi' fe'li -il qo'shimchasini olgan va majhul nisbatda turibdi."},
            {"q": "Qaysi qatorda sifatdosh qo'shimchalari berilgan?", "options": ["-ib, -gach, -may", "-gan, -yotgan, -ajak", "-ish, -moq, -uv", "-dir, -tir, -t"], "correct": 1, "exp": "-gan, -yotgan, -digan, -ajak sifatdosh hosil qiluvchi qo'shimchalardir."},
            {"q": "Qo'shma fe'lni aniqlang:", "options": ["Kelaverdi", "Yozib bo'ldi", "Kulimsiradi", "Bora-bora"], "correct": 1, "exp": "'Yozib bo'ldi' ikki qismdan iborat qo'shma fe'ldir."},
            {"q": "Qaysi so'z imlo qoidalariga ko'ra to'g'ri yozilgan?", "options": ["Mashxur", "Mashhur", "Mashur", "Mashg'ur"], "correct": 1, "exp": "'Mashhur' so'zida bo'g'iz tovushi 'h' ikki marta yoziladi."}
        ],
        "flashcards": [
            {"front": "O'zbek tilida nechta fe'l nisbati bor?", "back": "5 ta: Aniq, O'zlik, Majhul, Birgalik, Orttirma nisbatlar."},
            {"front": "Ravishdosh qanday so'roqlarga javob bo'ladi?", "back": "Qanday? qanday qilib? qay holatda? qachon? (Masalan: o'qib, kulgach)."},
            {"front": "Harakat nomi qo'shimchalari qaysilar?", "back": "-ish/-sh, -moq, -uv/-v (Masalan: o'qish, yozmoq, suzuv)."}
        ]
    },

    # 6. Adabiyot
    {
        "filename": "Otkan_Kunlar_Abdulla_Qodiriy.html",
        "title": "O'tkan Kunlar",
        "subtitle": "O'zbek milliy romanchiligining gultoji • To'liq asar va badiiy tahlil",
        "subject": "Adabiyot",
        "author": "Abdulla Qodiriy (Julqunboy)",
        "theme_color": "emerald",
        "icon": "fa-solid fa-feather-pointed",
        "chapters": [
            {
                "title": "1-bob. Abdulla Qodiriy va romanning yaratilish tarixi",
                "content": "<p>1925-1926-yillarda yaratilgan «O'tkan kunlar» romani o'zbek adabiyotidagi <b>birinchi roman</b> hisoblanadi. Asarda XIX asrning o'rtalaridagi Turkiston hayoti, xonliklar davridagi parokandalik, feodal tuzum ziddiyatlari va sof muhabbat fojiasi yuksak mahorat bilan tasvirlangan.</p><p>Muallif o'z asariga shunday deydi: <i>«Modomiki, biz yangi davrga oyoq qo'ydik, bas, biz har bir yo'sunda ham shu yangi davrning yangiliklari ketidan ergashamiz va shunga o'xshash dostonchilik, ro'monchilik va hikoyachilikda ham yangi tusda ish ko'rishga majburmiz»</i>.</p>",
                "key_points": [
                    "Roman ilk bor «Inqilob» jurnalida bosilgan.",
                    "Bosh qahramonlar: Otabek, Kumushbibi, Zaynab, Homid, Mirzakarim qutidor, O'zbek oyim, Hasanali."
                ]
            },
            {
                "title": "2-bob. Asar syujeti va qahramonlar xarakteri",
                "content": "<p>Toshkentlik savdogar Yusufbek hojining o'g'li Otabek Marg'ilonga safar qilib, u yerda Mirzakarim qutidorning qizi Kumushbibini sevib qoladi. Ularning sevgisi atrofida katta ijtimoiy va oilaviy ziddiyatlar, hasadgo'y Homidning fitnalari boshlanadi.</p><p>Otabekning onasi O'zbek oyimning injiqligi bilan Otabek Toshkentda Zaynabga uylanishga majbur bo'ladi. Ikki xotinlik fojiasi oqibatida Zaynab Kumushga zahar beradi va Kumush halok bo'ladi. Otabek esa vatan himoyasida dushmanga qarshi jangda mardlarcha halok bo'ladi.</p>",
                "key_points": [
                    "Otabek — ilg'or fikrli, vatanparvar, yangilikka intiluvchi ma'rifatli yigit.",
                    "Kumushbibi — o'zbek ayolining barcha go'zal fazilatlarini mujassam etgan timsol.",
                    "Romanning asosiy g'oyasi — xonliklar o'rtasidagi nifoq va qoloqlik xalqni halokatga yetaklashini ko'rsatish."
                ]
            }
        ],
        "quiz": [
            {"q": "O'zbek adabiyotidagi ilk roman qaysi va uning muallifi kim?", "options": ["«Mehrobdan chayon», A. Qodiriy", "«O'tkan kunlar», A. Qodiriy", "«Kecha va kunduz», Cho'lpon", "«Navoiy», Oybek"], "correct": 1, "exp": "1925-yilda yozilgan «O'tkan kunlar» o'zbek adabiyotidagi birinchi romandir."},
            {"q": "Otabekning vafodor va aqlli oqsoqoli kim edi?", "options": ["Hasanali", "Homid", "Rahmat", "Akram"], "correct": 0, "exp": "Hasanali oqsoqol Otabekka ham do'st, ham ota kabi mehribon ustoz edi."},
            {"q": "Kumushbibining zaharlanishiga kim sababchi bo'ladi?", "options": ["O'zbek oyim", "Zaynab", "Homid", "To'ybeka"], "correct": 1, "exp": "Kundoshlik hasadi va fitnalar ta'sirida Zaynab Kumushga zahar beradi."},
            {"q": "Otabek roman so'ngida qayerda halok bo'ladi?", "options": ["Marg'ilonda", "Toshkent qo'zg'olonida", "Dovon jangida dushman bosqiniga qarshi", "Chig'atoy qabristonida"], "correct": 2, "exp": "Otabek vatan ozodligi va el-yurt mudofaasi yo'lida jangda shahid bo'ladi."}
        ],
        "flashcards": [
            {"front": "«O'tkan kunlar» qachon kitob holida nashr qilingan?", "back": "1926-yilda Toshkentda birinchi marta to'liq kitob holida chop etilgan."},
            {"front": "Romanning epigrafida nima deyilgan?", "back": "«Tariximizning eng kir, qora kunlari bo'lgan keyingi 'xon zamonlari' yodnomasi...»"},
            {"front": "Kumushbibi qaysi shahardan bo'lgan?", "back": "Farg'ona vodiysidagi Marg'ilon shahridan."}
        ]
    },

    # 7. Ingliz tili
    {
        "filename": "English_Grammar_in_Use.html",
        "title": "English Grammar & Vocabulary",
        "subtitle": "Complete Reference and Interactive Practice for All Levels",
        "subject": "Ingliz tili",
        "author": "Raymond Murphy / Cambridge",
        "theme_color": "indigo",
        "icon": "fa-solid fa-language",
        "chapters": [
            {
                "title": "Unit 1. Present Simple vs Present Continuous",
                "content": "<p><b>Present Simple</b> is used for repeated actions, facts, habits, and permanent situations. Formula: <i>Subject + Verb (s/es)</i>. Signal words: <i>always, usually, often, every day, sometimes</i>.</p><p><b>Present Continuous</b> is used for actions happening right now at the moment of speaking or temporary situations. Formula: <i>Subject + am/is/are + Verb-ing</i>. Signal words: <i>now, at the moment, look!, listen!</i></p><div class='bg-indigo-50 p-4 rounded-xl text-indigo-900 text-sm space-y-1 my-2'><div>• I <b>play</b> football every Sunday. (Habit)</div><div>• Listen! She <b>is singing</b> a song. (Action happening now)</div></div>",
                "key_points": [
                    "Stative verbs (like, know, understand, believe) are not usually used in Continuous form.",
                    "Third person singular takes -s/-es: He works, She teaches."
                ]
            },
            {
                "title": "Unit 2. Past Simple vs Present Perfect",
                "content": "<p><b>Past Simple</b> expresses finished actions at a specific time in the past: <i>I visited Samarkand last year</i>. Signal words: <i>yesterday, ago, in 2020, last week</i>.</p><p><b>Present Perfect</b> links the past with the present; the action happened at an unspecified time, or has a direct result now: <i>I have lost my key (I don't have it now)</i>. Formula: <i>have/has + V3 (past participle)</i>.</p>",
                "key_points": [
                    "Regular verbs: add -ed (played, visited).",
                    "Irregular verbs: see, saw, seen | go, went, gone | write, wrote, written."
                ]
            },
            {
                "title": "Unit 3. Conditionals (If Clauses)",
                "content": "<p><b>Zero Conditional:</b> General truths. <i>If you heat water to 100°C, it boils.</i></p><p><b>First Conditional:</b> Real future possibilities. <i>If it rains tomorrow, I will stay at home.</i> (If + Present Simple, will + Verb).</p><p><b>Second Conditional:</b> Imaginary or unlikely situations now. <i>If I had a million dollars, I would travel the world.</i> (If + Past Simple, would + Verb).</p>",
                "key_points": [
                    "In First Conditional, do not use 'will' directly inside the 'if' clause.",
                    "Use 'were' instead of 'was' in Second conditional: 'If I were you...'"
                ]
            }
        ],
        "quiz": [
            {"q": "Choose the correct sentence: 'Look! The bus ...'", "options": ["comes", "is coming", "came", "has come"], "correct": 1, "exp": "Because of 'Look!', it indicates an action happening right now: 'is coming'."},
            {"q": "What is the Past Participle (V3) of the verb 'write'?", "options": ["wrote", "written", "writing", "writes"], "correct": 1, "exp": "write (V1) - wrote (V2) - written (V3)."},
            {"q": "Complete the conditional: 'If you study hard, you ... the exam.'", "options": ["pass", "will pass", "would pass", "passed"], "correct": 1, "exp": "First Conditional: If + Present Simple, will + Base Verb."},
            {"q": "'I ... in this city since 2015.' Which form is correct?", "options": ["live", "am living", "have lived", "lived"], "correct": 2, "exp": "'Since 2015' indicates Present Perfect: 'have lived'."}
        ],
        "flashcards": [
            {"front": "What is the formula of Present Perfect?", "back": "Subject + have / has + Past Participle (Verb 3)"},
            {"front": "Give the 3 forms of verb 'GO'", "back": "Go - Went - Gone"},
            {"front": "When do we use Second Conditional?", "back": "For hypothetical, imaginary, or unreal situations in the present or future."}
        ]
    },

    # 8. Geografiya
    {
        "filename": "Geografiya_7_sinf.html",
        "title": "Geografiya 7-sinf",
        "subtitle": "Materiklar va okeanlar tabiiy geografiyasi",
        "subject": "Geografiya",
        "author": "P. G'ulomov, H. Vahobov",
        "theme_color": "cyan",
        "icon": "fa-solid fa-earth-americas",
        "chapters": [
            {
                "title": "1-bob. Jahon okeani va uning qismlari",
                "content": "<p>Yer yuzasining taxminan 71% qismini Jahon okeani egallaydi. U to'rtta asosiy okeanga bo'linadi: <b>Tinch okeani</b> (eng katta va chuqur, Mariana botig'i - 11022 m), <b>Atlantika okeani</b>, <b>Hind okeani</b> va <b>Shimoliy Muz okeani</b> (eng kichik va sovuq).</p><p>Okean suvlari doimiy harakatda bo'lib, uning o'rtacha sho'rligi 35‰ (promille) ni tashkil qiladi. Qizil dengiz eng sho'r dengiz hisoblanadi (42‰).</p>",
                "key_points": [
                    "Mariana botig'i — Yer yuzidagi eng chuqur nuqta (11 022 m).",
                    "Issiq oqimlar (Golfstrim) iqlimni yumshatadi, sovuq oqimlar esa quruqlashtiradi."
                ]
            },
            {
                "title": "2-bob. Yer sharining eng yirik materiklari",
                "content": "<p>Yer yuzida 6 ta materik mavjud: <b>Yevrosiyo</b> (eng yirik, Yer quruqligining 1/3 qismi), <b>Afrika</b> (eng issiq), <b>Shimoliy Amerika</b>, <b>Janubiy Amerika</b> (eng sersuv, Amazonka daryosi), <b>Avstraliya</b> (eng mitti va qurg'oqchil) hamda <b>Antarktida</b> (eng sovuq va muz bilan qoplangan).</p>",
                "key_points": [
                    "Yevrosiyoda dunyodagi eng baland cho'qqi — Everest (Jomolungma, 8848 m) joylashgan.",
                    "Dunyodagi eng uzun daryo — Nil (Afrikada), eng sersuv daryo — Amazonka (Janubiy Amerikada)."
                ]
            }
        ],
        "quiz": [
            {"q": "Dunyo okeanidagi eng chuqur botiq qaysi?", "options": ["Yava botig'i", "Mariana botig'i", "Puerto-Riko botig'i", "Grenlandiya botig'i"], "correct": 1, "exp": "Mariana botig'i Tinch okeanida joylashgan bo'lib, chuqurligi taxminan 11 022 metr."},
            {"q": "Yer yuzidagi eng katta va eng baland materik qaysi?", "options": ["Afrika", "Yevrosiyo", "Shimoliy Amerika", "Janubiy Amerika"], "correct": 1, "exp": "Yevrosiyo eng yirik materik bo'lib, unda Yerning eng baland nuqtasi Everest joylashgan."},
            {"q": "Dunyodagi eng sersuv va havzasi eng katta daryo qaysi?", "options": ["Nil", "Amazonka", "Missisipi", "Yanszi"], "correct": 1, "exp": "Janubiy Amerikadagi Amazonka daryosi dunyodagi eng sersuv daryodir."},
            {"q": "Yer sharining eng qurg'oqchil va eng kichik materigi qaysi?", "options": ["Antarktida", "Avstraliya", "Afrika", "Janubiy Amerika"], "correct": 1, "exp": "Avstraliya eng mitti va qurg'oqchil materik hisoblanadi."}
        ],
        "flashcards": [
            {"front": "Jahon okeanining o'rtacha sho'rligi qancha?", "back": "35‰ (har 1 litr suvda 35 gramm tuz)."},
            {"front": "Yer yuzidagi eng baland cho'qqi qaysi?", "back": "Jomolungma (Everest) — 8848 metr, Himoloy tog'larida."},
            {"front": "Eng issiq materik qaysi?", "back": "Afrika materigi."}
        ]
    },

    # 9. Informatika
    {
        "filename": "Informatika_Python_8_sinf.html",
        "title": "Informatika va AT 8-sinf",
        "subtitle": "Algoritmlash va Python dasturlash tili asoslari",
        "subject": "Informatika",
        "author": "B. Boltayev, A. Rahimov",
        "theme_color": "emerald",
        "icon": "fa-brands fa-python",
        "chapters": [
            {
                "title": "1-bob. Algoritm tushunchasi va turlari",
                "content": "<p><b>Algoritm</b> — qo'yilgan maqsadga erishish yoki masalani yechish uchun bajarilishi lozim bo'lgan buyruqlarning aniq va ketma-ket tartibidir. Algoritm xossalari: aniqlik, tushunarlilik, diskretlik, ommaviylik va natijaviylik.</p><p>Algoritmlar 3 turga bo'linadi: <b>Chiziqli</b> (har bir buyruq ketma-ket bajariladi), <b>Tarmoqlanuvchi</b> (shartga qarab u yoki bu yo'nalish tanlanadi) va <b>Takrorlanuvchi (siklik)</b> (buyruqlar bir necha bor takrorlanadi).</p>",
                "key_points": [
                    "Blok-sxemada: Oval — boshlanish/tugash, Parallelogramm — kiritish/chiqarish, To'g'ri to'rtburchak — hisoblash, Romb — shartni tekshirish."
                ]
            },
            {
                "title": "2-bob. Python dasturlash tili asoslari",
                "content": "<p>Python — o'rganish oson, sodda va o'ta qudratli zamonaviy dasturlash tili. Guido van Rossum tomonidan yaratilgan. O'zgaruvchilar ma'lumotlarni xotirada saqlash uchun ishlatiladi.</p><div class='bg-slate-900 text-green-400 p-4 rounded-xl font-mono text-xs sm:text-sm space-y-1 my-3'><div># Ma'lumot turlari</div><div>ism = 'Husan'         # str (matn)</div><div>yosh = 16              # int (butun son)</div><div>baho = 4.8             # float (haqiqiy son)</div><div>talabami = True        # bool (mantiqiy)</div><div>print(f'{ism}ning yoshi {yosh}da')</div></div>",
                "key_points": [
                    "input() funksiyasi foydalanuvchidan ma'lumot oladi va doimo satr (str) qaytaradi.",
                    "Son kiritish uchun int(input()) yoki float(input()) ishlatiladi."
                ]
            },
            {
                "title": "3-bob. Shart operatorlari va Sikllar",
                "content": "<p><b>Shart operatori:</b> <code>if</code>, <code>elif</code> va <code>else</code> orqali dastur turli yo'nalishlarda ishlaydi. Pythonda bloklar probellar (indentation - 4 ta bo'shliq) orqali ajratiladi.</p><p><b>Sikllar:</b> <code>for</code> (aniq takrorlanishlar soni uchun) va <code>while</code> (shart to'g'ri bo'lib turguncha ishlash uchun).</p><div class='bg-slate-900 text-yellow-300 p-4 rounded-xl font-mono text-xs sm:text-sm space-y-1 my-3'><div>for i in range(1, 6):</div><div>&nbsp;&nbsp;&nbsp;&nbsp;print(f'{i}-qadam: Dasturlashni o'rganamiz!')</div></div>",
                "key_points": [
                    "Ro'yxatlar (list): mevalar = ['olma', 'anor', 'shaftoli']. Indeks 0 dan boshlanadi.",
                    "len() funksiyasi elementlar sonini sanaydi."
                ]
            }
        ],
        "quiz": [
            {"q": "Pythonda matnni ekranga chiqarish uchun qaysi funksiya ishlatiladi?", "options": ["echo()", "print()", "output()", "display()"], "correct": 1, "exp": "Pythonda konsolga ma'lumot chiqarish print() funksiyasi orqali bajariladi."},
            {"q": "x = 10; y = 3; print(x % y) dastur kodi qanday natija beradi?", "options": ["3.33", "3", "1", "0"], "correct": 2, "exp": "% operatori qoldiqli bo'lishni bajaradi: 10 ni 3 ga bo'lganda qoldiq 1 bo'ladi."},
            {"q": "Blok-sxemada shartni tekshirish qaysi geometrik shakl bilan belgilanadi?", "options": ["Doira", "To'g'ri to'rtburchak", "Romb", "Parallelogramm"], "correct": 2, "exp": "Romb belgisi tarmoqlanish va shartni ifodalashda qo'llaniladi."},
            {"q": "Pythonda qaysi ma'lumot turi mantiqiy (True yoki False) qiymat qabul qiladi?", "options": ["string", "integer", "boolean", "float"], "correct": 2, "exp": "bool (boolean) turi mantiqiy True yoki False qiymatlarga ega."}
        ],
        "flashcards": [
            {"front": "Algoritmning asosiy xossalari qaysilar?", "back": "Diskretlik, tushunarlilik, aniqlik, ommaviylik, natijaviylik."},
            {"front": "Pythonda ro'yxat (list) qanday qavs bilan ochiladi?", "back": "Kvadrat qavs bilan: [1, 2, 'salom']"},
            {"front": "int(input()) nima vazifani bajaradi?", "back": "Foydalanuvchi kiritgan satrli matnni butun songa o'tkazadi."}
        ]
    }
]

print("Kitoblar generatsiyasi boshlanmoqda...")
count = 0
for b in books_data:
    file_path = BOOKS_DIR / b["filename"]
    html_content = generate_book_html(b)
    file_path.write_text(html_content, encoding="utf-8")
    print(f"[OK] Yaratildi: {b['filename']} ({len(html_content)} bayt)")
    count += 1

print(f"Jami {count} ta yangi elektron kitob yaratildi!")
