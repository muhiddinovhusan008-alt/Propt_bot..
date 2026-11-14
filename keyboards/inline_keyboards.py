"""
Inline tugmalar (InlineKeyboardMarkup).
"""

from typing import List, Dict, Any, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_subjects_keyboard(action_prefix: str = "sub_lib") -> InlineKeyboardMarkup:
    """
    Fanlar ro'yxatini chiqaruvchi inline klaviatura.
    action_prefix:
    - 'sub_lib' (kutubxona uchun)
    - 'sub_quiz' (test uchun)
    - 'sub_facts' (faktlar uchun)
    - 'adm_book_sub' (admin kitob qo'shishi uchun)
    - 'adm_q_sub' (admin savol qo'shishi uchun)
    """
    builder = InlineKeyboardBuilder()

    # 10 ta asosiy fanlar
    subjects = [
        ("📐 Matematika", 1),
        ("⚡ Fizika", 2),
        ("🧪 Kimyo", 3),
        ("🌿 Biologiya", 4),
        ("🏛 Tarix", 5),
        ("✍️ Ona tili", 6),
        ("📜 Adabiyot", 7),
        ("🇬🇧 Ingliz tili", 8),
        ("🌍 Geografiya", 9),
        ("💻 Informatika", 10),
    ]

    for name, s_id in subjects:
        builder.button(text=name, callback_data=f"{action_prefix}:{s_id}")

    builder.adjust(2)  # Har qatorda 2 tadan tugma

    if action_prefix == "sub_lib":
        # Qidirish tugmasi
        builder.row(InlineKeyboardButton(text="🔍 Kitob qidirish", callback_data="search_books"))

    builder.row(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_main"))

    return builder.as_markup()


def get_grades_keyboard(subject_id: int, action_prefix: str = "lib_grade") -> InlineKeyboardMarkup:
    """
    Sinflar menyusi (5-11-sinflar) 2 ustunli qulay mobil dizaynda.
    action_prefix:
    - 'lib_grade': Foydalanuvchi kutubxona sinfini tanlashi uchun
    - 'adm_book_grade': Admin yangi kitob sinfini tanlashi uchun
    """
    builder = InlineKeyboardBuilder()
    grades = ["5-sinf", "6-sinf", "7-sinf", "8-sinf", "9-sinf", "10-sinf", "11-sinf"]

    for gr in grades:
        builder.button(text=f"🎓 {gr}", callback_data=f"{action_prefix}:{subject_id}:{gr}")

    builder.adjust(2)  # 2 ustunli chiroyli mobil ko'rinish

    if action_prefix == "adm_book_grade":
        builder.row(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:cancel"))
    else:
        builder.row(InlineKeyboardButton(text="⬅️ Fanlar ro'yxatiga", callback_data="back_to_subjects_lib"))
        builder.row(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_main"))

    return builder.as_markup()


def get_books_keyboard(books: List[Dict[str, Any]], subject_id: int, grade: str = "") -> InlineKeyboardMarkup:
    """Aynan tanlangan fan va sinfga biriktirilgan kitoblar ro'yxati."""
    builder = InlineKeyboardBuilder()

    for book in books:
        title_btn = f"📖 {book['title']}"
        builder.button(text=title_btn, callback_data=f"book_info:{book['id']}:{grade}")

    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="⬅️ Sinflar ro'yxatiga", callback_data=f"sub_lib:{subject_id}"))
    builder.row(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_main"))
    return builder.as_markup()


def get_empty_books_keyboard(subject_id: int) -> InlineKeyboardMarkup:
    """Sinfda kitoblar mavjud bo'lmaganda ko'rsatiladigan menyu."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Sinflar ro'yxatiga", callback_data=f"sub_lib:{subject_id}"))
    builder.row(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_main"))
    return builder.as_markup()


def get_biology_grades_keyboard() -> InlineKeyboardMarkup:
    """Biologiya fani bo'yicha sinflar tanlovi (eski havolalar mosligi uchun saqlangan)."""
    return get_grades_keyboard(subject_id=4, action_prefix="lib_grade")



def get_book_action_keyboard(
    book_id: int,
    subject_id: int,
    grade: str = "",
    has_file: bool = False,
    file_url: Optional[str] = None
) -> InlineKeyboardMarkup:
    """Kitobni ko'rish yoki yuklab olish harakatlari."""
    builder = InlineKeyboardBuilder()

    if has_file:
        builder.button(text="📥 PDF faylni yuklab olish", callback_data=f"download_book:{book_id}")
    if file_url:
        builder.button(text="🌐 Rasmiy onlayn nusxa", url=file_url)
    if not has_file and not file_url:
        builder.button(text="📥 Faylni qabul qilish", callback_data=f"download_book:{book_id}")

    builder.adjust(1)
    if grade:
        builder.row(InlineKeyboardButton(text="⬅️ Kitoblar ro'yxatiga", callback_data=f"lib_grade:{subject_id}:{grade}"))
    else:
        builder.row(InlineKeyboardButton(text="⬅️ Sinflar ro'yxatiga", callback_data=f"sub_lib:{subject_id}"))
    builder.row(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_main"))
    return builder.as_markup()


def get_quiz_count_keyboard(subject_id: int) -> InlineKeyboardMarkup:
    """Test savollari sonini tanlash (10, 20, 30 ta)."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔹 10 ta savol", callback_data=f"start_quiz:{subject_id}:10")
    builder.button(text="🔹 20 ta savol", callback_data=f"start_quiz:{subject_id}:20")
    builder.button(text="🔹 30 ta savol", callback_data=f"start_quiz:{subject_id}:30")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Fanlar ro'yxatiga qaytish", callback_data="back_to_subjects_quiz"))
    return builder.as_markup()


def get_quiz_options_keyboard(current_index: int, total_count: int) -> InlineKeyboardMarkup:
    """Testdagi 4 ta javob varianti (A, B, C, D)."""
    builder = InlineKeyboardBuilder()
    builder.button(text="A", callback_data="ans:A")
    builder.button(text="B", callback_data="ans:B")
    builder.button(text="C", callback_data="ans:C")
    builder.button(text="D", callback_data="ans:D")
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🛑 Testni to'xtatish", callback_data="stop_quiz"))
    return builder.as_markup()


def get_rating_menu_keyboard() -> InlineKeyboardMarkup:
    """O'quvchilar reytingi bo'limi inline menyusi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🏆 Umumiy Top-10", callback_data="rating:top")
    builder.button(text="📅 Haftalik Top-10", callback_data="rating:weekly")
    builder.button(text="⚡️ Eng faollar", callback_data="rating:active")
    builder.button(text="📍 Mening o'rnim", callback_data="rating:my_rank")
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main"))
    return builder.as_markup()


def get_daily_menu_keyboard() -> InlineKeyboardMarkup:
    """Kunlik bilim bo'limi menyusi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔬 Bugungi ilmiy fakt", callback_data="daily:fact")
    builder.button(text="❓ Kunlik bilim savoli (+5 ball)", callback_data="daily:question")
    builder.button(text="📚 Fanlar bo'yicha faktlar", callback_data="daily:subjects")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main"))
    return builder.as_markup()


def get_daily_question_keyboard(daily_q_id: int) -> InlineKeyboardMarkup:
    """Kunlik savolga javob variantlari."""
    builder = InlineKeyboardBuilder()
    builder.button(text="A", callback_data=f"daily_ans:{daily_q_id}:A")
    builder.button(text="B", callback_data=f"daily_ans:{daily_q_id}:B")
    builder.button(text="C", callback_data=f"daily_ans:{daily_q_id}:C")
    builder.button(text="D", callback_data=f"daily_ans:{daily_q_id}:D")
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Kunlik bilimga qaytish", callback_data="back_to_daily"))
    return builder.as_markup()


def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Shaxsiy profil menyusi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Ismni o'zgartirish", callback_data="edit_profile:name")
    builder.button(text="🎓 Sinfni o'zgartirish", callback_data="edit_profile:grade")
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main"))
    return builder.as_markup()


def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    """Admin maxsus boshqaruv paneli menyusi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="📚 Kitob qo‘shish", callback_data="admin:add_book")
    builder.button(text="🗑 Kitobni o‘chirish", callback_data="admin:del_book_menu")
    builder.button(text="✏️ Kitobni tahrirlash", callback_data="admin:edit_book_menu")
    builder.button(text="📖 Barcha kitoblarni ko‘rish", callback_data="admin:view_all:0")
    builder.button(text="📊 Statistika", callback_data="admin:stats")
    builder.adjust(2, 2, 1)
    builder.row(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back_to_main"))
    return builder.as_markup()


def get_admin_books_list_keyboard(
    books: List[Dict[str, Any]],
    offset: int = 0,
    action_type: str = "view",
    subject_id: Optional[int] = None
) -> InlineKeyboardMarkup:
    """Admin kitoblar ro'yxati (ko'rish, o'chirish yoki tahrirlash uchun)."""
    builder = InlineKeyboardBuilder()

    for book in books:
        prefix = "📖" if action_type == "view" else ("🗑" if action_type == "delete" else "✏️")
        btn_text = f"{prefix} {book['title']} ({book['grade']})"
        builder.button(text=btn_text, callback_data=f"adm_book_act:{action_type}:{book['id']}")

    builder.adjust(1)

    # Sahifalash (Pagination) tugmalari
    nav_btns = []
    if offset >= 8:
        nav_btns.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"adm_books_page:{action_type}:{offset - 8}:{subject_id or 0}"))
    if len(books) == 8:
        nav_btns.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"adm_books_page:{action_type}:{offset + 8}:{subject_id or 0}"))

    if nav_btns:
        builder.row(*nav_btns)

    builder.row(InlineKeyboardButton(text="🔙 Admin panelga", callback_data="admin:menu"))
    return builder.as_markup()


def get_admin_edit_fields_keyboard(book_id: int) -> InlineKeyboardMarkup:
    """Kitobni tahrirlashda qaysi maydonni o'zgartirishni tanlash."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Nomini o'zgartirish", callback_data=f"adm_edit_field:{book_id}:title")
    builder.button(text="🎓 Sinfini o'zgartirish", callback_data=f"adm_edit_field:{book_id}:grade")
    builder.button(text="📝 Tavsifini o'zgartirish", callback_data=f"adm_edit_field:{book_id}:desc")
    builder.button(text="📎 PDF faylni yangilash", callback_data=f"adm_edit_field:{book_id}:file")
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔙 Kitoblar ro'yxatiga", callback_data="admin:edit_book_menu"))
    builder.row(InlineKeyboardButton(text="🔙 Admin panelga", callback_data="admin:menu"))
    return builder.as_markup()


def get_admin_confirm_delete_keyboard(book_id: int) -> InlineKeyboardMarkup:
    """Kitobni o'chirishni tasdiqlash klaviaturasi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑 Ha, o'chirilsin", callback_data=f"adm_do_delete:{book_id}")
    builder.button(text="❌ Bekor qilish", callback_data="admin:del_book_menu")
    builder.adjust(2)
    return builder.as_markup()


def get_admin_cancel_keyboard() -> InlineKeyboardMarkup:
    """Admin amalini bekor qilish."""
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Bekor qilish", callback_data="admin:cancel")
    return builder.as_markup()


def get_back_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    """Oddiy orqaga qaytish tugmasi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Ortga", callback_data=callback_data)
    return builder.as_markup()


INSTAGRAM_URL = "https://www.instagram.com/muh1dd1nov_ai?psln=eTdsMGtodmgxZXlz"
ADMIN_USERNAME = "Muhiddinov_official"


def get_instagram_sub_keyboard() -> InlineKeyboardMarkup:
    """Instagram sahifaga obuna bo'lish tugmalari."""
    builder = InlineKeyboardBuilder()
    builder.button(text="📲 Instagram sahifaga obuna bo'lish", url=INSTAGRAM_URL)
    builder.button(text="✅ Obunani tasdiqlash", callback_data="check_insta_sub")
    builder.adjust(1)
    return builder.as_markup()


def get_contact_admin_keyboard() -> InlineKeyboardMarkup:
    """Administratorga to'g'ridan-to'g'ri havola beruvchi inline klaviatura."""
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Administratorga yozish (@Muhiddinov_official)", url=f"https://t.me/{ADMIN_USERNAME}")
    builder.button(text="🔙 Asosiy menyu", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

