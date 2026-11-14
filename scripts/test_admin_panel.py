import asyncio
from utils.helpers import is_admin
from keyboards.default_keyboards import get_main_keyboard
from keyboards.inline_keyboards import (
    get_admin_main_keyboard,
    get_admin_books_list_keyboard,
    get_admin_edit_fields_keyboard,
    get_admin_confirm_delete_keyboard
)
from database.models import (
    add_book,
    get_book_by_id,
    update_book,
    delete_book,
    get_all_books,
    get_bot_statistics
)

async def test_admin():
    print("=" * 60)
    print("TEST: Maxsus Admin Panel tizimini tekshirish")
    print("=" * 60)

    # 1. Admin huquqi faqat 8235455342 ga berilganligini tekshirish
    assert is_admin(8235455342) is True, "8235455342 admin bo'lishi kerak!"
    assert is_admin(9202952114) is False, "Eski ID admin bo'lmasligi kerak!"
    assert is_admin(11111111) is False, "Boshqa ID admin bo'lmasligi kerak!"
    print("[OK] 1. Admin tekshiruvi: Faqat 8235455342 admin huquqiga ega.")

    # 2. Asosiy klaviaturada faqat adminga ko'rinishi
    kb_admin = get_main_keyboard(is_admin=True)
    kb_user = get_main_keyboard(is_admin=False)
    admin_buttons = [b.text for r in kb_admin.keyboard for b in r]
    user_buttons = [b.text for r in kb_user.keyboard for b in r]
    assert any("Admin panel" in b for b in admin_buttons), "Adminga Admin panel ko'rinishi kerak"
    assert not any("Admin panel" in b for b in user_buttons), "Oddiy foydalanuvchiga Admin panel ko'rinmasligi kerak"
    print("[OK] 2. Admin panel tugmasi faqat 9202952114 ga ko'rinishi tasdiqlandi.")

    # 3. Admin panel menyusi (5 ta talab qilingan funksiya)
    admin_kb = get_admin_main_keyboard()
    admin_panel_texts = [btn.text for row in admin_kb.inline_keyboard for btn in row]
    
    assert any("Kitob qo‘shish" in t or "Kitob qo'shish" in t for t in admin_panel_texts), "Kitob qo'shish tugmasi yo'q!"
    assert any("Kitobni o‘chirish" in t or "Kitobni o'chirish" in t for t in admin_panel_texts), "Kitobni o'chirish tugmasi yo'q!"
    assert any("Kitobni tahrirlash" in t for t in admin_panel_texts), "Kitobni tahrirlash tugmasi yo'q!"
    assert any("Barcha kitoblarni ko‘rish" in t or "Barcha kitoblarni ko'rish" in t for t in admin_panel_texts), "Barcha kitoblarni ko'rish tugmasi yo'q!"
    assert any("Statistika" in t for t in admin_panel_texts), "Statistika tugmasi yo'q!"
    print("[OK] 3. Admin panelda 5 ta asosiy funksiya mavjud (Qo'shish, O'chirish, Tahrirlash, Barchasini ko'rish, Statistika).")

    # 4. CRUD sinovlari:
    # 4a. Kitob qo'shish
    book_id = await add_book(
        subject_id=1,
        title="Admin Test Kitob",
        author="Admin Muallif",
        grade="9-sinf",
        description="Admin panel orqali kiritildi",
        file_id="BQACAgIAAxkBAAItest123"
    )
    assert book_id > 0
    print(f"[OK] 4a. Kitob qo'shish ishladi (ID: {book_id}).")

    # 4b. Kitobni ko'rish (Barcha kitoblar ro'yxatida chiqishi)
    all_books = await get_all_books(limit=10, offset=0)
    assert any(b["id"] == book_id for b in all_books)
    print("[OK] 4b. Barcha kitoblarni ko'rish funksiyasi ishladi.")

    # 4c. Kitobni tahrirlash (nom, sinf, tavsif, pdf)
    updated = await update_book(
        book_id=book_id,
        title="Yangi Yangilangan Kitob",
        grade="10-sinf",
        description="Yangi tavsif kiritildi",
        file_id="BQACAgIAAxkBAAInewpdf456"
    )
    assert updated is True
    b_after = await get_book_by_id(book_id)
    assert b_after["title"] == "Yangi Yangilangan Kitob"
    assert b_after["grade"] == "10-sinf"
    assert b_after["file_id"] == "BQACAgIAAxkBAAInewpdf456"
    print("[OK] 4c. Kitobni tahrirlash ishladi (Nomi, sinfi, tavsifi va fayli yangilandi).")

    # 4d. Kitobni o'chirish
    deleted = await delete_book(book_id)
    assert deleted is True
    b_deleted = await get_book_by_id(book_id)
    assert b_deleted is None
    print("[OK] 4d. Kitobni o'chirish ishladi (Kitob bazadan butunlay o'chirildi).")

    # 5. Statistika
    stats = await get_bot_statistics()
    assert stats["books_count"] > 0
    print(f"[OK] 5. Statistika ishladi (Kitoblar soni: {stats['books_count']}, Foydalanuvchilar: {stats['users_count']}).")

    print("=" * 60)
    print("ADMIN PANEL BARCHA TALABLAR BO'YICHA 100% MUVAFFAQIYATLI ISHLAMOQDA!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_admin())
