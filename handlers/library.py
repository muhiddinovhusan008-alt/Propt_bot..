"""
Elektron kutubxona moduli:
Fanlar ro'yxati, kitoblar katalogi, qidirish va yuklab olish.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from config import BOOKS_DIR
from database import (
    get_subjects,
    get_subject_by_id,
    get_books_by_subject,
    get_books_by_subject_and_grade,
    get_book_by_id,
    search_books,
    increment_book_downloads
)
from keyboards import (
    get_subjects_keyboard,
    get_grades_keyboard,
    get_books_keyboard,
    get_empty_books_keyboard,
    get_book_action_keyboard,
    get_main_keyboard,
    get_cancel_keyboard
)
from states import SearchBookStates
from utils import escape_html, is_admin

router = Router()


@router.message(F.text == "📚 Elektron kutubxona")
async def show_library(message: Message):
    """Kutubxona bosh sahifasi: 10 ta fan ro'yxati."""
    text = (
        "<b>📚 ELEKTRON KUTUBXONA</b>\n\n"
        "O'zingizga kerakli fanni tanlang yoki qidiruv orqali kitob nomini kiriting:"
    )
    await message.answer(text, reply_markup=get_subjects_keyboard(action_prefix="sub_lib"), parse_mode="HTML")


@router.callback_query(F.data == "back_to_subjects_lib")
async def back_to_subjects_lib(call: CallbackQuery):
    """Sinflar yoki kitoblar ro'yxatidan fanlar ro'yxatiga qaytish."""
    text = (
        "<b>📚 ELEKTRON KUTUBXONA</b>\n\n"
        "O'zingizga kerakli fanni tanlang yoki qidiruv orqali kitob nomini kiriting:"
    )
    await call.message.edit_text(text, reply_markup=get_subjects_keyboard(action_prefix="sub_lib"), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data.startswith("sub_lib:"))
async def show_subject_grades(call: CallbackQuery):
    """Tanlangan fan bo'yicha 5-11-sinflar menyusini ko'rsatish."""
    subject_id = int(call.data.split(":")[1])
    subject = await get_subject_by_id(subject_id)

    sub_name = subject["name"] if subject else "Fan"
    sub_icon = subject["icon"] if subject else "📖"

    text = (
        f"{sub_icon} <b>{sub_name.upper()} — SINFLARNI TANLASH</b>\n\n"
        f"Qaysi sinf darsliklarini ko'rmoqchisiz?\n"
        f"<i>Kerakli sinfni tanlang:</i>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_grades_keyboard(subject_id=subject_id, action_prefix="lib_grade"),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data.startswith("lib_grade:") | F.data.startswith("bio_grade:"))
async def show_grade_books(call: CallbackQuery):
    """Tanlangan fan va aynan shu sinfga biriktirilgan kitoblarni ko'rsatish."""
    if call.data.startswith("bio_grade:"):
        subject_id = 4
        grade_num = call.data.split(":")[1]
        grade = f"{grade_num}-sinf"
    else:
        parts = call.data.split(":")
        subject_id = int(parts[1])
        grade = parts[2] if len(parts) > 2 else "5-sinf"

    subject = await get_subject_by_id(subject_id)
    sub_name = subject["name"] if subject else "Fan"
    sub_icon = subject["icon"] if subject else "📖"

    # Aynan shu fan va shu sinfga tegishli kitoblarni olish
    books = await get_books_by_subject_and_grade(subject_id, grade)

    if not books:
        text = (
            f"{sub_icon} <b>{sub_name} — {grade}</b>\n\n"
            f"ℹ️ <b>Hozircha bu sinf uchun kitoblar mavjud emas.</b>\n\n"
            f"Tez orada ushbu sinf uchun yangi darslik va materiallar joylanadi!"
        )
        await call.message.edit_text(
            text,
            reply_markup=get_empty_books_keyboard(subject_id),
            parse_mode="HTML"
        )
        await call.answer()
        return

    text = (
        f"{sub_icon} <b>{sub_name} — {grade}</b>\n\n"
        f"Aynan <b>{grade} {sub_name}</b> faniga oid mavjud darslik va kitoblar:\n\n"
        f"<i>Kitob haqida to'liq ma'lumot olish yoki yuklab olish uchun uning ustiga bosing:</i>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_books_keyboard(books, subject_id, grade),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data.startswith("book_info:"))
async def show_book_info(call: CallbackQuery):
    """Bitta kitob haqida to'liq ma'lumot."""
    parts = call.data.split(":")
    book_id = int(parts[1])
    grade = parts[2] if len(parts) > 2 else ""

    book = await get_book_by_id(book_id)

    if not book:
        await call.answer("Kitob topilmadi!", show_alert=True)
        return

    if not grade:
        grade = book.get("grade", "")

    title = escape_html(book["title"])
    author = escape_html(book["author"])
    grade_display = escape_html(book["grade"])
    desc = escape_html(book["description"])
    downloads = book["downloads_count"]
    subject_name = escape_html(book["subject_name"])

    text = (
        f"📖 <b>Kitob:</b> {title}\n"
        f"✍️ <b>Muallif:</b> {author}\n"
        f"📂 <b>Fan:</b> {subject_name}\n"
        f"🎓 <b>Sinf / Bosqich:</b> {grade_display}\n"
        f"📥 <b>Yuklab olingan:</b> {downloads} marta\n\n"
        f"📝 <b>Tavsif:</b>\n<i>{desc or 'Tavsif mavjud emas.'}</i>"
    )

    has_file = bool(book.get("file_id"))
    file_url = book.get("file_url")

    await call.message.edit_text(
        text,
        reply_markup=get_book_action_keyboard(
            book_id=book_id,
            subject_id=book["subject_id"],
            grade=grade,
            has_file=has_file,
            file_url=file_url
        ),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data.startswith("download_book:"))
async def download_book_handler(call: CallbackQuery):
    """Kitob faylini foydalanuvchiga yuborish."""
    book_id = int(call.data.split(":")[1])
    book = await get_book_by_id(book_id)

    if not book:
        await call.answer("Kitob topilmadi!", show_alert=True)
        return

    # Yuklab olish hisoblagichini oshirish
    await increment_book_downloads(book_id)

    file_id = book.get("file_id")
    title = escape_html(book["title"])
    author = escape_html(book.get("author", ""))
    grade = escape_html(book.get("grade", ""))

    if file_id:
        local_file = BOOKS_DIR / file_id
        if local_file.exists():
            # Serverdagi mahalliy elektron darslik / HTML faylini yuborish
            file_to_send = FSInputFile(
                path=local_file,
                filename=file_id
            )
            caption = (
                f"📚 <b>{title}</b>\n\n"
                f"✍️ <b>Muallif:</b> {author}\n"
                f"🎓 <b>Sinf/Bosqich:</b> {grade}\n\n"
                f"✨ <i>«Bilim Kutubxonasi» orqali taqdim etildi.</i>\n"
                f"📱 <i>Faylni yuklab olib, brauzeringizda (Chrome, Safari va b.) interaktiv tarzda o'qishingiz mumkin!</i>"
            )
            await call.message.answer_document(
                document=file_to_send,
                caption=caption,
                parse_mode="HTML"
            )
            await call.answer("Kitob muvaffaqiyatli yuborildi!")
            return
        else:
            # Telegram file_id orqali yuborish
            try:
                await call.message.answer_document(
                    document=file_id,
                    caption=f"📚 <b>{title}</b>\n\n«Bilim Kutubxonasi» orqali yuklab olindi.",
                    parse_mode="HTML"
                )
                await call.answer("Kitob yuborildi!")
                return
            except Exception as e:
                pass

    # Agar fayl serverda ham, Telegramda ham bo'lmasa:
    file_url = book.get("file_url")
    if file_url:
        await call.message.answer(
            f"📄 <b>{title}</b>\n\n"
            f"Ushbu darslikni quyidagi havola orqali onlayn o'qishingiz yoki PDF nusxasini yuklab olishingiz mumkin:\n"
            f"🔗 <a href='{file_url}'>Rasmiy elektron nusxani yuklab olish</a>",
            parse_mode="HTML"
        )
        await call.answer()
    else:
        await call.message.answer(
            f"📄 <b>{title}</b>\n\n"
            f"Ushbu darslik elektron katalogga kiritilgan. Administrator tez orada to'liq PDF faylni ham yuklaydi!\n\n"
            f"<i>Yuklab olishlar hisoblagichi qayd etildi.</i>",
            parse_mode="HTML"
        )
        await call.answer()


# ==================== KITOBLARNI QIDIRISH ====================

@router.callback_query(F.data == "search_books")
async def start_search_books(call: CallbackQuery, state: FSMContext):
    """Kitob qidirishni boshlash."""
    await state.set_state(SearchBookStates.waiting_for_query)
    await call.message.answer(
        "🔍 Qidirayotgan kitobingiz yoki muallifning nomini kiriting:",
        reply_markup=get_cancel_keyboard()
    )
    await call.answer()


@router.message(SearchBookStates.waiting_for_query)
async def process_search_books(message: Message, state: FSMContext):
    """Kitob qidirish natijasini chiqarish."""
    query = message.text.strip()
    await state.clear()

    admin_flag = is_admin(message.from_user.id)

    if len(query) < 2:
        await message.answer(
            "Qidiruv so'zi juda qisqa (kamida 2 ta belgi kiriting).",
            reply_markup=get_main_keyboard(is_admin=admin_flag)
        )
        return

    results = await search_books(query)

    if not results:
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙 Kutubxonaga qaytish", callback_data="back_to_subjects_lib")
        await message.answer(
            f"🔍 «<b>{escape_html(query)}</b>» so'rovi bo'yicha hech qanday kitob topilmadi.",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        return

    builder = InlineKeyboardBuilder()
    for book in results:
        builder.button(
            text=f"📖 {book['title']} ({book['grade']})",
            callback_data=f"book_info:{book['id']}"
        )
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Kutubxonaga qaytish", callback_data="back_to_subjects_lib"))

    await message.answer(
        f"🔍 «<b>{escape_html(query)}</b>» bo'yicha topilgan kitoblar ({len(results)} ta):\n"
        f"<i>Batafsil ko'rish uchun tanlang:</i>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
