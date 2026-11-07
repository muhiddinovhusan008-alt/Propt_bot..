import asyncio
import aiosqlite
from pathlib import Path

DB_PATH = Path("database/bilim_kutubxonasi.db")

book_updates = [
    # (subject_name, title_match, file_id, file_url)
    ("Matematika", "%Algebra - 7-sinf%", "Algebra_7_sinf.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    ("Fizika", "%Fizika - 9-sinf%", "Fizika_8_sinf.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    ("Kimyo", "%Kimyo - 8-sinf%", "Kimyo_8_sinf.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    ("Biologiya", "%Zoologiya - 7-sinf%", "Zoologiya_7_sinf_interaktiv.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    ("Tarix", "%O'zbekiston tarixi - 8-sinf%", "Ozbekiston_Tarixi_8_sinf.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    ("Ona tili", "%Ona tili - 7-sinf%", "Ona_Tili_7_sinf.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    ("Adabiyot", "%O'tkan kunlar%", "Otkan_Kunlar_Abdulla_Qodiriy.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    ("Ingliz tili", "%English Grammar in Use%", "English_Grammar_in_Use.html", "https://dictionary.cambridge.org/"),
    ("Geografiya", "%Materiklar va okeanlar%", "Geografiya_7_sinf.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
    ("Informatika", "%Informatika va AT - 8-sinf%", "Informatika_Python_8_sinf.html", "https://ziyouz.com/kutubxona/category/11-maktab-darsliklari"),
]

async def update_books():
    async with aiosqlite.connect(DB_PATH) as db:
        for sub_name, title_pattern, file_id, file_url in book_updates:
            cursor = await db.execute("""
                UPDATE books 
                SET file_id = ?, file_url = ?
                WHERE title LIKE ?
            """, (file_id, file_url, title_pattern))
            print(f"Updated: {sub_name} ({title_pattern}) -> rows affected: {cursor.rowcount}")
        await db.commit()
    print("Database kitoblari yangilandi!")

if __name__ == "__main__":
    asyncio.run(update_books())
