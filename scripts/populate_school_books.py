import asyncio
import aiosqlite
from pathlib import Path

DB_PATH = Path("database/bilim_kutubxonasi.db")

# Har bir fanga tegishli yangi darsliklar ro'yxati
# Format: (subject_id, title, author, grade, description, file_id, file_url)
new_books = [
    # 1. Matematika (id=1)
    (1, "Matematika - 6-sinf", "M. Mirzaxmedov, A. Rahimqoriyev", "6-sinf", "Oddiy va o'nli kasrlar, proporsiya, ratsional sonlar va geometriya asoslari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (1, "Algebra - 9-sinf", "Sh. Alimov, O. Xolmuhamedov", "9-sinf", "Kvadrat tenglamalar, tengsizliklar, sonli ketma-ketliklar va progressiyalar.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (1, "Algebra va analiz asoslari - 10-sinf", "M. Mirzaxmedov", "10-sinf", "Trigonometrik funksiyalar, teskari trigonometriya va hosila hisoblash asoslari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (1, "Algebra va analiz asoslari - 11-sinf", "M. Mirzaxmedov", "11-sinf", "Boshlang'ich funksiya, integral, stereometriya va ehtimollar nazariyasi.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),

    # 2. Fizika (id=2)
    (2, "Fizika - 7-sinf", "P. Habibullayev, A. Boydedayev", "7-sinf", "Mexanik harakat, modda tuzilishi, zichlik, jismning og'irligi va bosim hodisalari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (2, "Fizika - 8-sinf", "P. Habibullayev, A. Boydedayev", "8-sinf", "Issiqlik hodisalari, zaryadlar, Om qonuni va elektr zanjirlari.", "Fizika_8_sinf.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (2, "Fizika - 11-sinf", "K. Tursunmetov", "11-sinf", "Elektromagnit tebranishlar va to'lqinlar, to'lqin optikasi, kvant va atom fizikasi.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),

    # 3. Kimyo (id=3)
    (3, "Kimyo - 7-sinf", "I. Asqarov, N. To'xtayev", "7-sinf", "Kimyoning boshlang'ich tushunchalari, kimyoviy elementlar va laboratoriya asboblari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (3, "Organik kimyo - 10-sinf", "I. Asqarov", "10-sinf", "To'yingan va to'yinmagan uglevodorodlar, spirtlar, aldegidlar va organik birikmalar.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (3, "Umumiy kimyo - 11-sinf", "I. Asqarov", "11-sinf", "Kimyoviy muvozanat, eritmalarning elektrokimyosi, metallar va yuqori molekulyar moddalar.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),

    # 4. Biologiya (id=4)
    (4, "Tabiatshunoslik va Botanika - 5-sinf", "O. Pratov", "5-sinf", "Tirik tabiatning xilma-xilligi, hujayra va o'simlik organlari tuzilishi.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (4, "Biologiya (Sitologiya va genetika) - 9-sinf", "A. Zikiryayev", "9-sinf", "Hujayra biologiyasi, oqsillar sintezi, Mendel qonunlari va irsiyat asoslari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (4, "Umumiy biologiya - 10-sinf", "A. G'ofurov", "10-sinf", "Tiriklikning molekulyar darajasi, organizmlarning ko'payishi va evolyutsion ta'limot.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (4, "Umumiy biologiya va ekologiya - 11-sinf", "A. G'ofurov", "11-sinf", "Biotsenoz, ekotizimlar, biosfera va tabiatni muhofaza qilishning biologik asoslari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),

    # 5. Tarix (id=5)
    (5, "Tarixdan hikoyalar - 5-sinf", "T. Boboyev", "5-sinf", "Qadimgi Movarounnahr shaharlari, afsonalar va buyuk ajdodlarimiz merosi.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (5, "Qadimgi dunyo tarixi - 6-sinf", "A. Sagdullayev", "6-sinf", "Ibtidoiy jamoa tuzumi, Qadimgi Misr, Mesopotamiya, Qadimgi Yunoniston va Rim imperiyasi.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (5, "O'zbekiston tarixi (O'rta asrlar) - 7-sinf", "A. Muhammadjonov", "7-sinf", "Arab xalifaligi davri, Somoniylar, Qoraxoniylar, Xorazmshohlar va Amir Temur saltanati.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (5, "O'zbekiston tarixi (XIX - XX asrlar) - 10-sinf", "Q. Rajabov", "10-sinf", "Chor Rossiyasi mustamlakachiligi davri, jadidchilik harakati va ma'rifatparvarlik.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (5, "O'zbekistonning eng yangi tarixi - 11-sinf", "Q. Rajabov", "11-sinf", "Mustaqil O'zbekiston Respublikasining tashkil topishi va zamonaviy taraqqiyot bosqichlari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),

    # 6. Ona tili (id=6)
    (6, "Ona tili - 5-sinf", "N. Mahmudov", "5-sinf", "Fonetika, nutq tovushlari, harflar, so'z ma'nolari va to'g'ri yozish qoidalari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (6, "Ona tili - 6-sinf", "A. Nurmonov", "6-sinf", "So'z yasalishi, asosiy so'z turkumlari: ot, sifat, son va olmosh grammatikasi.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (6, "Ona tili - 8-sinf", "M. Qodirov", "8-sinf", "Sintaksis: so'z birikmasi, sodda gap va uning bosh hamda ikkinchi darajali bo'laklari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (6, "Ona tili va nutq madaniyati - 10-sinf", "N. Mahmudov", "10-sinf", "Stilistika (uslubiyat), matn tahlili va adabiy nutq me'yorlari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (6, "Ona tili - 11-sinf", "N. Mahmudov", "11-sinf", "Matn tilshunosligi, muloqot madaniyati va leksikografiya asoslari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),

    # 7. Adabiyot (id=7)
    (7, "Adabiyot - 5-sinf", "S. Ahmedov", "5-sinf", "O'zbek xalq og'zaki ijodi, maqollar, topishmoqlar, ertaklar va qisqa hikoyalar.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (7, "Adabiyot - 6-sinf", "S. Ahmedov", "6-sinf", "Alisher Navoiy, Zahriddin Muhammad Bobur g'azallari va zamonaviy dostonlar.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (7, "Adabiyot - 7-sinf", "Q. Yo'ldoshev", "7-sinf", "Mumtoz va zamonaviy o'zbek adabiyoti parchalari, badiiy asar tahlili.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (7, "Adabiyot - 9-sinf", "Q. Yo'ldoshev, B. Qosimov", "9-sinf", "Behbudiy, Munavvarqori, Cho'lpon asarlari va roman tahlillari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (7, "O'zbek adabiyoti - 10-sinf", "B. Qosimov", "10-sinf", "Abdulla Qodiriy 'O'tkan kunlar', Fitrat dramalari va Oybek ijodi.", "Otkan_Kunlar_Abdulla_Qodiriy.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (7, "Jahon va o'zbek adabiyoti - 11-sinf", "B. Qosimov", "11-sinf", "Dante, Shekspir, Gyote, Pushkin va XX asr o'zbek she'riyati durdonalari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),

    # 8. Ingliz tili (id=8)
    (8, "English - 6-sinf", "Cambridge / O'zbekiston", "6-sinf", "English for 6th grade: reading comprehension, basic past tenses and vocabulary.", None, "https://dictionary.cambridge.org/"),
    (8, "English - Teen World 7-sinf", "Cambridge / O'zbekiston", "7-sinf", "Teen World: communication, modal verbs, reading and writing exercises.", None, "https://dictionary.cambridge.org/"),
    (8, "English - 8-sinf", "Cambridge / O'zbekiston", "8-sinf", "Comparative degrees, future tenses, intermediate grammar and audio dialogues.", None, "https://dictionary.cambridge.org/"),
    (8, "English - Prepare! 9-sinf", "Cambridge / O'zbekiston", "9-sinf", "Prepare! course: passive voice, conditionals and situational conversations.", None, "https://dictionary.cambridge.org/"),
    (8, "English for Success - 10-sinf", "Cambridge / O'zbekiston", "10-sinf", "Academic reading, essay structures, phrasal verbs and idioms.", None, "https://dictionary.cambridge.org/"),
    (8, "English B2 Level - 11-sinf", "Cambridge / O'zbekiston", "11-sinf", "B2 level grammar, international exam preparation and fluent speaking topics.", None, "https://dictionary.cambridge.org/"),

    # 9. Geografiya (id=9)
    (9, "Tabiiy geografiya boshlang'ich kursi - 5-sinf", "P. G'ulomov", "5-sinf", "Yerning shakli va o'lchamlari, xaritalar, masshtab va azimut tushunchalari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (9, "Materiklar va okeanlar geografiyasi - 6-sinf", "P. G'ulomov", "6-sinf", "Qit'alar tabiati, okeanlar relyingi, shamollar va tabiiy zonalar.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (9, "O'zbekiston tabiiy geografiyasi - 8-sinf", "P. G'ulomov", "8-sinf", "O'zbekistonning tabiati, iqlim mintaqalari, Amudaryo va Sirdaryo havzalari, foydali qazilmalar.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (9, "O'zbekiston iqtisodiy va ijtimoiy geografiyasi - 9-sinf", "A. Soliyev", "9-sinf", "O'zbekiston viloyatlari, sanoat tarmoqlari, transport va tashqi iqtisodiy aloqalar.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (9, "Jahon ijtimoiy-iqtisodiy geografiyasi - 10-sinf", "A. Qayumov", "10-sinf", "Dunyo siyosiy xaritasi, xalqaro mehnat taqsimoti va iqtisodiy rivojlangan davlatlar.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (9, "Global geografiya va geosiyosat - 11-sinf", "A. Qayumov", "11-sinf", "Globallashuv jarayonlari, demografik portlash, ekologiya va barqaror rivojlanish.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),

    # 10. Informatika (id=10)
    (10, "Informatika va axborot texnologiyalari - 5-sinf", "B. Boltayev", "5-sinf", "Kompyuter qurilmalari, sichqoncha va klaviatura bilan ishlash, dasturlar tushunchasi.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (10, "Informatika va AT - 6-sinf", "B. Boltayev", "6-sinf", "Word matn muharriri, fayllar tizimi va axborot xavfsizligi madaniyati.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (10, "Informatika va AT - 7-sinf", "B. Boltayev", "7-sinf", "Excel elektron jadvallari, formulalar, diagrammalar va Powerpoint taqdimotlari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (10, "Informatika va AT (Veb dasturlash) - 9-sinf", "B. Boltayev", "9-sinf", "HTML5 teglari, CSS uslublari va shaxsiy veb-sahifalar yaratish amaliyoti.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (10, "Informatika va AT (Ma'lumotlar bazasi) - 10-sinf", "B. Boltayev", "10-sinf", "Relyatsion ma'lumotlar bazasi, jadvallar va SQL so'rovlar tili asoslari.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    (10, "Informatika va axborot xavfsizligi - 11-sinf", "B. Boltayev", "11-sinf", "Kiberxavfsizlik asoslari, axborotni shifrlash, tarmoq protokollari va zamonaviy IT.", None, "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari")
]

async def populate():
    async with aiosqlite.connect(DB_PATH) as db:
        inserted = 0
        for sub_id, title, author, grade, desc, file_id, file_url in new_books:
            # Agar bu kitob hali bazada bo'lmasa, qo'shamiz
            cursor = await db.execute(
                "SELECT id FROM books WHERE subject_id = ? AND grade = ? AND title = ?",
                (sub_id, grade, title)
            )
            row = await cursor.fetchone()
            if not row:
                await db.execute(
                    """INSERT INTO books (subject_id, title, author, grade, description, file_id, file_url)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (sub_id, title, author, grade, desc, file_id, file_url)
                )
                inserted += 1
        await db.commit()
        print(f"Jami {inserted} ta yangi darslik bazaga muvaffaqiyatli qo'shildi!")

if __name__ == "__main__":
    asyncio.run(populate())
