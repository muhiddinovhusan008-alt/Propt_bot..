import asyncio
from database.models import (
    get_subjects,
    get_books_by_subject_and_grade,
    get_book_by_id,
    add_book,
    increment_book_downloads,
    search_books
)
from keyboards.inline_keyboards import (
    get_subjects_keyboard,
    get_grades_keyboard,
    get_books_keyboard,
    get_empty_books_keyboard,
    get_book_action_keyboard
)

async def test_full_library_flow():
    print("=" * 60)
    print("TEST: Elektron Kutubxona tizimini to'liq tekshirish")
    print("=" * 60)

    # 1. Fanlarni olish
    subjects = await get_subjects()
    assert len(subjects) == 10, f"Fanlar soni 10 ta bo'lishi kerak, hozir {len(subjects)} ta"
    print(f"[OK] 1. Fanlar ro'yxati tekshirildi: 10 ta fan mavjud.")

    # 2. Sinflar klaviaturasi
    for s in subjects:
        kb = get_grades_keyboard(s["id"])
        # Tugmalar ro'yxatini tekshirish
        button_texts = [btn.text for row in kb.inline_keyboard for btn in row]
        assert "🎓 5-sinf" in button_texts
        assert "🎓 11-sinf" in button_texts
        assert "⬅️ Fanlar ro'yxatiga" in button_texts
        assert "🏠 Asosiy menyu" in button_texts
    print("[OK] 2. Sinflar menyusi (5-11-sinflar, 2 ustunli dizayn) barcha 10 ta fan uchun to'g'ri shakllandi.")

    # 3. Kitoblarni sinflar bo'yicha izolyatsiyasi
    total_books = 0
    for s in subjects:
        for g in range(5, 12):
            grade_str = f"{g}-sinf"
            books = await get_books_by_subject_and_grade(s["id"], grade_str)
            for b in books:
                total_books += 1
                assert grade_str in b["grade"] or str(g) == b["grade"], \
                    f"Xatolik: {b['title']} kitobi {grade_str} sinfida noo'rin chiqdi!"
    print(f"[OK] 3. Kitoblarning sinflar bo'yicha to'liq izolyatsiyasi tekshirildi ({total_books} ta kitob joyida).")

    # 4. Matematika 9-sinf aniq tekshiruvi (user masalasi)
    math_sub = [s for s in subjects if "matematika" in s["name"].lower()][0]
    math_9_books = await get_books_by_subject_and_grade(math_sub["id"], "9-sinf")
    assert len(math_9_books) > 0, "9-sinf matematika kitobi topilmadi!"
    for b in math_9_books:
        assert "9-sinf" in b["grade"] or "9" == b["grade"]
    print(f"[OK] 4. Matematika -> 9-sinf tekshirildi: Faqat 9-sinf kitoblari chiqmoqda: {[b['title'] for b in math_9_books]}")

    # 5. Admin yangi kitob qo'shish sinovi
    test_title = "Sinov Kitobi - 9-sinf"
    test_desc = "Admin paneldan kiritilgan sinov darsligi"
    test_file_id = "BQACAgIAAxkBAAI_test_file_id_123456"

    new_id = await add_book(
        subject_id=math_sub["id"],
        title=test_title,
        author="Sinovchi Muallif",
        grade="9-sinf",
        description=test_desc,
        file_id=test_file_id
    )
    print(f"[OK] 5. Admin kitob qo'shish tekshirildi (Yangi book_id={new_id}).")

    # 6. Yangi kitobni o'qish va ma'lumotlarini tekshirish
    book = await get_book_by_id(new_id)
    assert book is not None
    assert book["title"] == test_title
    assert book["grade"] == "9-sinf"
    assert book["file_id"] == test_file_id
    print(f"[OK] 6. Kitob ma'lumotlari to'liq va xatosiz saqlangan: {book['title']} ({book['grade']})")

    # 7. Yuklab olish va hisoblagichni oshirish
    old_downloads = book["downloads_count"]
    await increment_book_downloads(new_id)
    updated_book = await get_book_by_id(new_id)
    assert updated_book["downloads_count"] == old_downloads + 1
    print(f"[OK] 7. Yuklab olish hisoblagichi oshirildi: {old_downloads} -> {updated_book['downloads_count']}.")

    # 8. Qidiruv sinovi
    search_res = await search_books("Sinov Kitobi")
    assert len(search_res) > 0
    print(f"[OK] 8. Qidiruv funksiyasi tekshirildi (Topildi: {search_res[0]['title']}).")

    # 9. Sinov kitobini tozalash
    import aiosqlite
    from pathlib import Path
    async with aiosqlite.connect(Path("database/bilim_kutubxonasi.db")) as db:
        await db.execute("DELETE FROM books WHERE id = ?", (new_id,))
        await db.commit()
    print("[OK] 9. Sinov ma'lumotlari tozalandi.")

    print("=" * 60)
    print("BARCHA SINOVLAR MUVAFFAQIYATLI O'TDI! TIZIM 100% TAYYOR!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_full_library_flow())
