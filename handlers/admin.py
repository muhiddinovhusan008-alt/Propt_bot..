"""
Administrator paneli moduli:
Kitob va PDF yuklash, test savollari qo'shish/o'chirish,
kunlik fakt/savol qo'shish, bot statistikasi va xabar yuborish (broadcast).
"""

import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from database import (
    get_bot_statistics,
    add_book,
    delete_book,
    update_book,
    get_all_books,
    get_book_by_id,
    add_question,
    get_questions_by_subject,
    delete_question,
    add_daily_fact,
    add_daily_question,
    get_subjects,
    get_subject_by_id,
    get_all_user_ids
)
from keyboards import (
    get_admin_main_keyboard,
    get_admin_cancel_keyboard,
    get_admin_books_list_keyboard,
    get_admin_edit_fields_keyboard,
    get_admin_confirm_delete_keyboard,
    get_subjects_keyboard,
    get_grades_keyboard,
    get_main_keyboard
)
from states import (
    AdminAddBookStates,
    AdminEditBookStates,
    AdminDeleteBookStates,
    AdminAddQuestionStates,
    AdminAddFactStates,
    AdminAddDailyQuestionStates,
    AdminBroadcastStates
)
from utils import is_admin, escape_html

router = Router()


# ==================== ADMIN PANEL ASOSIY MENYU ====================

@router.message(Command("admin"))
@router.message(F.text == "⚙️ Admin panel")
async def show_admin_panel(message: Message, state: FSMContext):
    """Admin panelini ochish."""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Kechirasiz, ushbu bo'lim faqat administratorlar uchun mo'ljallangan.")
        return

    await state.clear()
    text = (
        "<b>⚙️ ADMINISTRATOR BOSHQARUV PANELI</b>\n\n"
        "Quyidagi boshqaruv funksiyalaridan birini tanlang:"
    )
    await message.answer(text, reply_markup=get_admin_main_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "admin:cancel")
async def admin_cancel(call: CallbackQuery, state: FSMContext):
    """Admin jarayonini bekor qilish."""
    await state.clear()
    await call.message.edit_text(
        "Amal bekor qilindi.\n<b>⚙️ ADMINISTRATOR BOSHQARUV PANELI</b>",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )
    await call.answer("Bekor qilindi")


# ==================== STATISTIKA ====================

@router.callback_query(F.data == "admin:stats")
async def show_stats(call: CallbackQuery):
    """Bot statistikasini chiqarish."""
    if not is_admin(call.from_user.id):
        await call.answer("Ruxsat yo'q!", show_alert=True)
        return

    stats = await get_bot_statistics()

    text = (
        "<b>📊 BOTNING TO'LIQ STATISTIKASI</b>\n\n"
        f"👥 <b>Jami foydalanuvchilar:</b> {stats['users_count']} nafar\n"
        f"📂 <b>Faol fanlar:</b> {stats['subjects_count']} ta\n"
        f"📚 <b>Elektron darsliklar:</b> {stats['books_count']} ta\n"
        f"📥 <b>Kitoblar yuklab olinishi:</b> {stats['total_downloads']} marta\n"
        f"📝 <b>Bazada test savollari:</b> {stats['questions_count']} ta\n"
        f"🎯 <b>Ishlangan testlar soni:</b> {stats['tests_count']} ta\n"
        f"⭐️ <b>O'quvchilarga berilgan jami ballar:</b> {stats['total_scores']} ball\n\n"
        f"<i>Tizim normal holatda ishlamoqda.</i>"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Yangilash", callback_data="admin:stats")
    builder.button(text="🔙 Admin panelga", callback_data="admin:menu")
    builder.adjust(1)

    await call.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "admin:menu")
async def return_to_admin_menu(call: CallbackQuery, state: FSMContext):
    """Admin panel bosh menyusiga qaytish."""
    await state.clear()
    await call.message.edit_text(
        "<b>⚙️ ADMINISTRATOR BOSHQARUV PANELI</b>\n\n"
        "Quyidagi boshqaruv funksiyalaridan birini tanlang:",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


# ==================== KITOB VA PDF YUKLASH ====================

@router.callback_query(F.data == "admin:add_book")
async def start_add_book(call: CallbackQuery, state: FSMContext):
    """Kitob qo'shish jarayonini boshlash: fanni tanlash."""
    if not is_admin(call.from_user.id):
        return

    await state.set_state(AdminAddBookStates.waiting_for_subject)
    await call.message.edit_text(
        "<b>📚 YANGI KITOB YUKLASH (1/5)</b>\n\n"
        "Kitob qaysi fanga tegishli? Kerakli fanni tanlang:",
        reply_markup=get_subjects_keyboard(action_prefix="adm_book_sub"),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(AdminAddBookStates.waiting_for_subject, F.data.startswith("adm_book_sub:"))
async def process_book_subject(call: CallbackQuery, state: FSMContext):
    """Kitob fani tanlandi, endi sinf so'raladi."""
    subject_id = int(call.data.split(":")[1])
    subject = await get_subject_by_id(subject_id)
    sub_name = subject["name"] if subject else "Fan"

    await state.update_data(subject_id=subject_id, subject_name=sub_name)
    await state.set_state(AdminAddBookStates.waiting_for_grade)

    await call.message.edit_text(
        f"<b>📚 YANGI KITOB YUKLASH (2/5)</b>\n\n"
        f"Tanlangan fan: <b>{sub_name}</b>\n\n"
        f"Kitob qaysi <b>sinfga</b> mo'ljallangan? Quyidagi sinflardan birini tanlang:",
        reply_markup=get_grades_keyboard(subject_id=subject_id, action_prefix="adm_book_grade"),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(AdminAddBookStates.waiting_for_grade, F.data.startswith("adm_book_grade:"))
async def process_book_grade_callback(call: CallbackQuery, state: FSMContext):
    """Sinf inline tugma orqali tanlandi, kitob nomi so'raladi."""
    parts = call.data.split(":")
    grade = parts[2] if len(parts) > 2 else "Barcha sinflar"

    await state.update_data(grade=grade)
    await state.set_state(AdminAddBookStates.waiting_for_title)

    await call.message.edit_text(
        f"<b>📚 YANGI KITOB YUKLASH (3/5)</b>\n\n"
        f"Tanlangan sinf: <b>{grade}</b>\n\n"
        f"Kitob yoki darslikning <b>to'liq nomini</b> kiriting (masalan: <i>Algebra - 9-sinf</i>):",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(AdminAddBookStates.waiting_for_grade)
async def process_book_grade_message(message: Message, state: FSMContext):
    """Sinf matn ko'rinishida yuborilsa."""
    grade = message.text.strip()
    await state.update_data(grade=grade)
    await state.set_state(AdminAddBookStates.waiting_for_title)

    await message.answer(
        f"<b>📚 YANGI KITOB YUKLASH (3/5)</b>\n\n"
        f"Tanlangan sinf: <b>{grade}</b>\n\n"
        f"Kitob yoki darslikning <b>to'liq nomini</b> kiriting (masalan: <i>Algebra - 9-sinf</i>):",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )


@router.message(AdminAddBookStates.waiting_for_title)
async def process_book_title(message: Message, state: FSMContext):
    """Kitob nomi kiritildi, qisqacha tavsif so'raladi."""
    title = message.text.strip()
    await state.update_data(title=title)
    await state.set_state(AdminAddBookStates.waiting_for_desc)

    await message.answer(
        "<b>📚 YANGI KITOB YUKLASH (4/5)</b>\n\n"
        "Kitob haqida <b>qisqacha ma'lumot (tavsif)</b> kiriting (yoki '.' deb yuboring):",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )


@router.message(AdminAddBookStates.waiting_for_desc)
async def process_book_desc(message: Message, state: FSMContext):
    """Tavsif kiritildi, endi PDF fayl so'raladi."""
    desc = message.text.strip()
    if desc == ".":
        desc = ""
    await state.update_data(description=desc)
    await state.set_state(AdminAddBookStates.waiting_for_file)

    await message.answer(
        "<b>📚 YANGI KITOB YUKLASH (5/5)</b>\n\n"
        "Kitobning <b>PDF faylini (Hujjat/Document)</b> yuboring yoki yuklab olish havolasini yozing:\n"
        "<i>(Agar hozircha fayl bo'lmasa, 'faylsiz' deb yozishingiz mumkin)</i>",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )


@router.message(AdminAddBookStates.waiting_for_file)
async def process_book_file(message: Message, state: FSMContext):
    """Kitob faylini saqlash va jarayonni yakunlash."""
    data = await state.get_data()
    file_id = None
    file_url = None

    if message.document:
        file_id = message.document.file_id
    elif message.text:
        text = message.text.strip()
        if text.startswith("http://") or text.startswith("https://"):
            file_url = text

    await add_book(
        subject_id=data["subject_id"],
        title=data["title"],
        author=data.get("author", "Noma'lum"),
        grade=data.get("grade", "Barcha sinflar"),
        description=data.get("description", ""),
        file_id=file_id,
        file_url=file_url
    )

    await state.clear()
    await message.answer(
        f"✅ <b>Kitob muvaffaqiyatli saqlandi va elektron kutubxonaga qo'shildi!</b>\n\n"
        f"📂 <b>Fan:</b> {escape_html(data.get('subject_name', 'Fan'))}\n"
        f"🎓 <b>Sinf:</b> {escape_html(data.get('grade', ''))}\n"
        f"📖 <b>Nomi:</b> {escape_html(data['title'])}\n"
        f"📝 <b>Tavsif:</b> {escape_html(data.get('description') or 'Kiritilmagan')}\n"
        f"📎 <b>PDF Fayl:</b> {'Biriktirildi ✅' if file_id else (file_url if file_url else 'Faylsiz')}",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )


# ==================== BARCHA KITOBLARNI KO'RISH ====================

@router.callback_query(F.data.startswith("admin:view_all:"))
async def view_all_books(call: CallbackQuery):
    """Barcha mavjud kitoblar ro'yxatini ko'rish."""
    if not is_admin(call.from_user.id):
        await call.answer("Ruxsat yo'q!", show_alert=True)
        return

    offset = int(call.data.split(":")[2])
    books = await get_all_books(limit=8, offset=offset)

    if not books and offset == 0:
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙 Admin panelga", callback_data="admin:menu")
        await call.message.edit_text(
            "<b>📖 BARCHA KITOBLAR</b>\n\nHozircha bazada kitoblar mavjud emas.",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        await call.answer()
        return

    page_num = (offset // 8) + 1
    text = (
        f"<b>📖 BARCHA DARSLIK VA KITOBLAR (Sahifa {page_num})</b>\n\n"
        f"Kitob haqida to'liq ma'lumot olish yoki boshqarish uchun ustiga bosing:"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_admin_books_list_keyboard(books, offset=offset, action_type="view"),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_books_page:"))
async def switch_books_page(call: CallbackQuery):
    """Kitoblar ro'yxati sahifasini almashtirish."""
    if not is_admin(call.from_user.id):
        return

    parts = call.data.split(":")
    action_type = parts[1]
    offset = int(parts[2])
    sub_id = int(parts[3]) if len(parts) > 3 and parts[3] != "0" else None

    books = await get_all_books(limit=8, offset=offset, subject_id=sub_id)
    page_num = (offset // 8) + 1

    titles = {
        "view": f"<b>📖 BARCHA DARSLIK VA KITOBLAR (Sahifa {page_num})</b>",
        "delete": f"<b>🗑 KITOBNI O'CHIRISH (Sahifa {page_num})</b>\n\nO'chirmoqchi bo'lgan kitobingizni tanlang:",
        "edit": f"<b>✏️ KITOBNI TAHRIRLASH (Sahifa {page_num})</b>\n\nTahrirlamoqchi bo'lgan kitobingizni tanlang:"
    }
    header = titles.get(action_type, f"Kitoblar ro'yxati (Sahifa {page_num})")

    await call.message.edit_text(
        header,
        reply_markup=get_admin_books_list_keyboard(books, offset=offset, action_type=action_type, subject_id=sub_id),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_book_act:"))
async def handle_admin_book_action(call: CallbackQuery):
    """Kitob tanlanganda (ko'rish, o'chirish yoki tahrirlash)."""
    if not is_admin(call.from_user.id):
        return

    parts = call.data.split(":")
    action_type = parts[1]
    book_id = int(parts[2])

    book = await get_book_by_id(book_id)
    if not book:
        await call.answer("Kitob topilmadi!", show_alert=True)
        return

    title = escape_html(book["title"])
    author = escape_html(book.get("author", "Noma'lum"))
    subject_name = escape_html(book.get("subject_name", "Fan"))
    grade = escape_html(book.get("grade", ""))
    desc = escape_html(book.get("description") or "Kiritilmagan")
    downloads = book.get("downloads_count", 0)
    has_pdf = bool(book.get("file_id")) or bool(book.get("file_url"))

    if action_type == "view":
        text = (
            f"<b>📖 KITOB TAFSILOTLARI (ID: {book_id})</b>\n\n"
            f"📖 <b>Nomi:</b> {title}\n"
            f"✍️ <b>Muallif:</b> {author}\n"
            f"📂 <b>Fan:</b> {subject_name}\n"
            f"🎓 <b>Sinf:</b> {grade}\n"
            f"📥 <b>Yuklab olingan:</b> {downloads} marta\n"
            f"📎 <b>PDF Fayl:</b> {'Biriktirilgan ✅' if has_pdf else 'Mavjud emas ❌'}\n\n"
            f"📝 <b>Tavsif:</b>\n<i>{desc}</i>"
        )
        builder = InlineKeyboardBuilder()
        builder.button(text="✏️ Tahrirlash", callback_data=f"adm_book_act:edit:{book_id}")
        builder.button(text="🗑 O'chirish", callback_data=f"adm_book_act:delete:{book_id}")
        builder.button(text="🔙 Kitoblar ro'yxatiga", callback_data="admin:view_all:0")
        builder.button(text="🔙 Admin panelga", callback_data="admin:menu")
        builder.adjust(2, 1, 1)

        await call.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
        await call.answer()

    elif action_type == "delete":
        text = (
            f"<b>🗑 KITOBNI O'CHIRISHNI TASDIQLAYSIZMI?</b>\n\n"
            f"📖 <b>Nomi:</b> {title}\n"
            f"📂 <b>Fan:</b> {subject_name}\n"
            f"🎓 <b>Sinf:</b> {grade}\n\n"
            f"⚠️ <i>Haqiqatan ham ushbu kitobni o'chirib tashlamoqchimisiz? Ushbu amalni bekor qilib bo'lmaydi!</i>"
        )
        await call.message.edit_text(text, reply_markup=get_admin_confirm_delete_keyboard(book_id), parse_mode="HTML")
        await call.answer()

    elif action_type == "edit":
        text = (
            f"<b>✏️ KITOBNI TAHRIRLASH (ID: {book_id})</b>\n\n"
            f"📖 <b>Nomi:</b> {title}\n"
            f"📂 <b>Fan:</b> {subject_name}\n"
            f"🎓 <b>Sinf:</b> {grade}\n"
            f"📎 <b>PDF:</b> {'Mavjud ✅' if has_pdf else 'Mavjud emas ❌'}\n"
            f"📝 <b>Tavsif:</b> <i>{desc}</i>\n\n"
            f"<i>Qaysi ma'lumotni o'zgartirmoqchisiz? Quyidagilardan birini tanlang:</i>"
        )
        await call.message.edit_text(text, reply_markup=get_admin_edit_fields_keyboard(book_id), parse_mode="HTML")
        await call.answer()


# ==================== KITOBNI O'CHIRISH ====================

@router.callback_query(F.data == "admin:del_book_menu")
async def show_delete_books_menu(call: CallbackQuery):
    """O'chirish uchun kitoblar ro'yxati."""
    if not is_admin(call.from_user.id):
        await call.answer("Ruxsat yo'q!", show_alert=True)
        return

    books = await get_all_books(limit=8, offset=0)
    if not books:
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙 Admin panelga", callback_data="admin:menu")
        await call.message.edit_text(
            "<b>🗑 KITOBNI O'CHIRISH</b>\n\nBazada o'chirish uchun kitoblar mavjud emas.",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        await call.answer()
        return

    text = (
        "<b>🗑 KITOBNI O'CHIRISH BO'LIMI</b>\n\n"
        "O'chirmoqchi bo'lgan kitobingiz ustiga bosing:"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_admin_books_list_keyboard(books, offset=0, action_type="delete"),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_do_delete:"))
async def confirm_and_delete_book(call: CallbackQuery):
    """Kitobni bazadan o'chirishni ijro etish."""
    if not is_admin(call.from_user.id):
        return

    book_id = int(call.data.split(":")[1])
    success = await delete_book(book_id)

    if success:
        await call.answer("✅ Kitob muvaffaqiyatli o'chirildi!", show_alert=True)
    else:
        await call.answer("❌ Kitob topilmadi yoki allaqachon o'chirilgan.", show_alert=True)

    # Qayta o'chirish ro'yxatiga qaytish
    await show_delete_books_menu(call)


# ==================== KITOBNI TAHRIRLASH ====================

@router.callback_query(F.data == "admin:edit_book_menu")
async def show_edit_books_menu(call: CallbackQuery):
    """Tahrirlash uchun kitoblar ro'yxati."""
    if not is_admin(call.from_user.id):
        await call.answer("Ruxsat yo'q!", show_alert=True)
        return

    books = await get_all_books(limit=8, offset=0)
    if not books:
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙 Admin panelga", callback_data="admin:menu")
        await call.message.edit_text(
            "<b>✏️ KITOBNI TAHRIRLASH</b>\n\nBazada tahrirlash uchun kitoblar mavjud emas.",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        await call.answer()
        return

    text = (
        "<b>✏️ KITOBNI TAHRIRLASH BO'LIMI</b>\n\n"
        "Tahrirlamoqchi bo'lgan kitobingiz ustiga bosing:"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_admin_books_list_keyboard(books, offset=0, action_type="edit"),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_edit_field:"))
async def start_edit_field(call: CallbackQuery, state: FSMContext):
    """Kitobning tanlangan maydonini tahrirlashni boshlash."""
    if not is_admin(call.from_user.id):
        return

    parts = call.data.split(":")
    book_id = int(parts[1])
    field = parts[2]

    await state.update_data(edit_book_id=book_id)

    if field == "title":
        await state.set_state(AdminEditBookStates.waiting_for_new_title)
        await call.message.edit_text(
            "✏️ Kitobning <b>yangi to'liq nomini</b> kiriting:",
            reply_markup=get_admin_cancel_keyboard(),
            parse_mode="HTML"
        )
    elif field == "grade":
        await state.set_state(AdminEditBookStates.waiting_for_new_grade)
        await call.message.edit_text(
            "🎓 Kitob uchun <b>yangi sinfni</b> tanlang:",
            reply_markup=get_grades_keyboard(subject_id=0, action_prefix="adm_set_grade"),
            parse_mode="HTML"
        )
    elif field == "desc":
        await state.set_state(AdminEditBookStates.waiting_for_new_desc)
        await call.message.edit_text(
            "📝 Kitob uchun <b>yangi tavsif</b> kiriting (yoki '.' deb yuboring):",
            reply_markup=get_admin_cancel_keyboard(),
            parse_mode="HTML"
        )
    elif field == "file":
        await state.set_state(AdminEditBookStates.waiting_for_new_file)
        await call.message.edit_text(
            "📎 Kitobning <b>yangi PDF faylini</b> (Hujjat/Document ko'rinishida) yuboring:",
            reply_markup=get_admin_cancel_keyboard(),
            parse_mode="HTML"
        )
    await call.answer()


@router.message(AdminEditBookStates.waiting_for_new_title)
async def process_new_book_title(message: Message, state: FSMContext):
    """Yangi kitob nomini saqlash."""
    new_title = message.text.strip()
    data = await state.get_data()
    book_id = data.get("edit_book_id")

    await update_book(book_id=book_id, title=new_title)
    await state.clear()
    await message.answer(
        f"✅ Kitob nomi muvaffaqiyatli yangilandi:\n<b>{escape_html(new_title)}</b>",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(AdminEditBookStates.waiting_for_new_grade, F.data.startswith("adm_set_grade:"))
async def process_new_book_grade_cb(call: CallbackQuery, state: FSMContext):
    """Yangi sinf inline tugma orqali tanlandi."""
    parts = call.data.split(":")
    new_grade = parts[2] if len(parts) > 2 else "Barcha sinflar"
    data = await state.get_data()
    book_id = data.get("edit_book_id")

    await update_book(book_id=book_id, grade=new_grade)
    await state.clear()
    await call.message.edit_text(
        f"✅ Kitob sinfi muvaffaqiyatli yangilandi: <b>{escape_html(new_grade)}</b>",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(AdminEditBookStates.waiting_for_new_grade)
async def process_new_book_grade_msg(message: Message, state: FSMContext):
    """Yangi sinf matn orqali kiritildi."""
    new_grade = message.text.strip()
    data = await state.get_data()
    book_id = data.get("edit_book_id")

    await update_book(book_id=book_id, grade=new_grade)
    await state.clear()
    await message.answer(
        f"✅ Kitob sinfi muvaffaqiyatli yangilandi: <b>{escape_html(new_grade)}</b>",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )


@router.message(AdminEditBookStates.waiting_for_new_desc)
async def process_new_book_desc(message: Message, state: FSMContext):
    """Yangi tavsifni saqlash."""
    new_desc = message.text.strip()
    if new_desc == ".":
        new_desc = ""
    data = await state.get_data()
    book_id = data.get("edit_book_id")

    await update_book(book_id=book_id, description=new_desc)
    await state.clear()
    await message.answer(
        f"✅ Kitob tavsifi muvaffaqiyatli yangilandi:\n<i>{escape_html(new_desc or 'Bo‘sh')}</i>",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )


@router.message(AdminEditBookStates.waiting_for_new_file)
async def process_new_book_file(message: Message, state: FSMContext):
    """Yangi PDF faylni saqlash."""
    data = await state.get_data()
    book_id = data.get("edit_book_id")

    file_id = None
    file_url = None
    if message.document:
        file_id = message.document.file_id
    elif message.text and (message.text.startswith("http://") or message.text.startswith("https://")):
        file_url = message.text.strip()

    if not file_id and not file_url:
        await message.answer("Iltimos, PDF hujjat yoki havola yuboring (yoki bekor qilish tugmasini bosing):")
        return

    await update_book(book_id=book_id, file_id=file_id, file_url=file_url)
    await state.clear()
    await message.answer(
        "✅ Kitob PDF fayli muvaffaqiyatli yangilandi va saqlandi!",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )


# ==================== TEST SAVOLLARI QO'SHISH ====================

@router.callback_query(F.data == "admin:add_question")
async def start_add_question(call: CallbackQuery, state: FSMContext):
    """Test savoli qo'shish: fanni tanlash."""
    if not is_admin(call.from_user.id):
        return

    await state.set_state(AdminAddQuestionStates.waiting_for_subject)
    await call.message.edit_text(
        "<b>📝 YANGI TEST SAVOLI QO'SHISH (1/7)</b>\n\n"
        "Savol qaysi fanga tegishli ekanligini tanlang:",
        reply_markup=get_subjects_keyboard(action_prefix="adm_q_sub"),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(AdminAddQuestionStates.waiting_for_subject, F.data.startswith("adm_q_sub:"))
async def process_question_subject(call: CallbackQuery, state: FSMContext):
    """Fan tanlandi, savol matni so'raladi."""
    subject_id = int(call.data.split(":")[1])
    await state.update_data(subject_id=subject_id)
    await state.set_state(AdminAddQuestionStates.waiting_for_question_text)

    await call.message.edit_text(
        "<b>📝 YANGI TEST SAVOLI QO'SHISH (2/7)</b>\n\n"
        "<b>Savol matnini</b> kiriting:",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(AdminAddQuestionStates.waiting_for_question_text)
async def process_q_text(message: Message, state: FSMContext):
    """Savol matni kiritildi, A varianti so'raladi."""
    await state.update_data(question_text=message.text.strip())
    await state.set_state(AdminAddQuestionStates.waiting_for_option_a)
    await message.answer("<b>A</b> variantini kiriting:", reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminAddQuestionStates.waiting_for_option_a)
async def process_opt_a(message: Message, state: FSMContext):
    await state.update_data(option_a=message.text.strip())
    await state.set_state(AdminAddQuestionStates.waiting_for_option_b)
    await message.answer("<b>B</b> variantini kiriting:", reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminAddQuestionStates.waiting_for_option_b)
async def process_opt_b(message: Message, state: FSMContext):
    await state.update_data(option_b=message.text.strip())
    await state.set_state(AdminAddQuestionStates.waiting_for_option_c)
    await message.answer("<b>C</b> variantini kiriting:", reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminAddQuestionStates.waiting_for_option_c)
async def process_opt_c(message: Message, state: FSMContext):
    await state.update_data(option_c=message.text.strip())
    await state.set_state(AdminAddQuestionStates.waiting_for_option_d)
    await message.answer("<b>D</b> variantini kiriting:", reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminAddQuestionStates.waiting_for_option_d)
async def process_opt_d(message: Message, state: FSMContext):
    await state.update_data(option_d=message.text.strip())
    await state.set_state(AdminAddQuestionStates.waiting_for_correct_option)

    builder = InlineKeyboardBuilder()
    builder.button(text="A", callback_data="adm_correct:A")
    builder.button(text="B", callback_data="adm_correct:B")
    builder.button(text="C", callback_data="adm_correct:C")
    builder.button(text="D", callback_data="adm_correct:D")
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:cancel"))

    await message.answer(
        "Qaysi variant <b>to'g'ri javob</b> hisoblanadi? (Tugmani bosing):",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


@router.callback_query(AdminAddQuestionStates.waiting_for_correct_option, F.data.startswith("adm_correct:"))
async def process_correct_option(call: CallbackQuery, state: FSMContext):
    """To'g'ri javob tanlandi, izoh so'raladi."""
    correct_opt = call.data.split(":")[1].upper()
    await state.update_data(correct_option=correct_opt)
    await state.set_state(AdminAddQuestionStates.waiting_for_explanation)

    await call.message.edit_text(
        f"To'g'ri javob: <b>{correct_opt}</b>.\n\n"
        "Endi savol uchun <b>tushuntirish / yechim izohini</b> kiriting (yoki '.' deb yuboring):",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(AdminAddQuestionStates.waiting_for_explanation)
async def process_q_explanation(message: Message, state: FSMContext):
    """Savol to'liq saqlanadi."""
    expl = message.text.strip()
    if expl == ".":
        expl = ""

    data = await state.get_data()
    await add_question(
        subject_id=data["subject_id"],
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=expl
    )

    await state.clear()
    await message.answer(
        "✅ <b>Yangi test savoli muvaffaqiyatli saqlandi!</b>\n\n"
        f"❓ <b>Savol:</b> {escape_html(data['question_text'])}\n"
        f"🎯 <b>To'g'ri javob:</b> {data['correct_option']}",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )


# ==================== TEST SAVOLLARINI O'CHIRISH ====================

@router.callback_query(F.data == "admin:del_question")
async def choose_subject_to_delete_q(call: CallbackQuery):
    """Savol o'chirish uchun fanni tanlash."""
    if not is_admin(call.from_user.id):
        return

    text = "<b>🗑 QAYSI FAN SAVOLLARINI O'CHIRMOQCHISIZ?</b>\n\nFanni tanlang:"
    await call.message.edit_text(text, reply_markup=get_subjects_keyboard(action_prefix="adm_del_sub"), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data.startswith("adm_del_sub:"))
async def list_questions_for_deletion(call: CallbackQuery):
    """Fanning oxirgi savollarini ro'yxat qilish."""
    subject_id = int(call.data.split(":")[1])
    questions = await get_questions_by_subject(subject_id=subject_id, limit=8)

    if not questions:
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙 Admin panelga", callback_data="admin:menu")
        await call.message.edit_text("Ushbu fanda hozircha savollar yo'q.", reply_markup=builder.as_markup())
        await call.answer()
        return

    builder = InlineKeyboardBuilder()
    for q in questions:
        preview = q["question_text"][:35] + ("..." if len(q["question_text"]) > 35 else "")
        builder.button(text=f"❌ {preview}", callback_data=f"adm_do_del_q:{q['id']}:{subject_id}")

    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Admin panelga", callback_data="admin:menu"))

    await call.message.edit_text(
        "<b>O'chirmoqchi bo'lgan savolingiz ustiga bosing:</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_do_del_q:"))
async def execute_delete_question(call: CallbackQuery):
    """Savolni bazadan o'chirish."""
    parts = call.data.split(":")
    q_id = int(parts[1])
    subject_id = int(parts[2])

    await delete_question(q_id)
    await call.answer("Savol muvaffaqiyatli o'chirildi!", show_alert=True)

    # Ro'yxatni yangilash
    questions = await get_questions_by_subject(subject_id=subject_id, limit=8)
    builder = InlineKeyboardBuilder()
    for q in questions:
        preview = q["question_text"][:35] + ("..." if len(q["question_text"]) > 35 else "")
        builder.button(text=f"❌ {preview}", callback_data=f"adm_do_del_q:{q['id']}:{subject_id}")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Admin panelga", callback_data="admin:menu"))

    await call.message.edit_text(
        "<b>Savol o'chirildi! Yana o'chirish uchun tanlang:</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


# ==================== KUNLIK FAKT QO'SHISH ====================

@router.callback_query(F.data == "admin:add_fact")
async def start_add_fact(call: CallbackQuery, state: FSMContext):
    """Fakt qo'shishni boshlash: fanni tanlash."""
    if not is_admin(call.from_user.id):
        return

    await state.set_state(AdminAddFactStates.waiting_for_subject)
    await call.message.edit_text(
        "<b>💡 ILMIY FAKT QO'SHISH (1/3)</b>\n\nFanni tanlang:",
        reply_markup=get_subjects_keyboard(action_prefix="adm_fact_sub"),
        parse_mode="HTML"
    )
    await call.answer()


@router.callback_query(AdminAddFactStates.waiting_for_subject, F.data.startswith("adm_fact_sub:"))
async def process_fact_subject(call: CallbackQuery, state: FSMContext):
    subject_id = int(call.data.split(":")[1])
    await state.update_data(subject_id=subject_id)
    await state.set_state(AdminAddFactStates.waiting_for_title)

    await call.message.edit_text(
        "<b>💡 ILMIY FAKT QO'SHISH (2/3)</b>\n\nFaktning <b>sarlavhasini</b> kiriting:",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(AdminAddFactStates.waiting_for_title)
async def process_fact_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AdminAddFactStates.waiting_for_content)
    await message.answer(
        "<b>💡 ILMIY FAKT QO'SHISH (3/3)</b>\n\nFaktning <b>to'liq matnini</b> kiriting:",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )


@router.message(AdminAddFactStates.waiting_for_content)
async def process_fact_content(message: Message, state: FSMContext):
    content = message.text.strip()
    data = await state.get_data()

    await add_daily_fact(
        title=data["title"],
        content=content,
        subject_id=data["subject_id"]
    )
    await state.clear()
    await message.answer(
        "✅ <b>Yangi ilmiy fakt muvaffaqiyatli saqlandi!</b>",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )


# ==================== KUNLIK SAVOL QO'SHISH ====================

@router.callback_query(F.data == "admin:add_daily_q")
async def start_add_daily_q(call: CallbackQuery, state: FSMContext):
    """Kunlik savol qo'shish."""
    if not is_admin(call.from_user.id):
        return

    await state.set_state(AdminAddDailyQuestionStates.waiting_for_text)
    await call.message.edit_text(
        "<b>❓ YANGI KUNLIK SAVOL QO'SHISH</b>\n\nSavol matnini kiriting:",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(AdminAddDailyQuestionStates.waiting_for_text)
async def process_daily_q_text(message: Message, state: FSMContext):
    await state.update_data(question_text=message.text.strip())
    await state.set_state(AdminAddDailyQuestionStates.waiting_for_option_a)
    await message.answer("<b>A</b> variantini kiriting:", reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminAddDailyQuestionStates.waiting_for_option_a)
async def process_daily_opt_a(message: Message, state: FSMContext):
    await state.update_data(option_a=message.text.strip())
    await state.set_state(AdminAddDailyQuestionStates.waiting_for_option_b)
    await message.answer("<b>B</b> variantini kiriting:", reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminAddDailyQuestionStates.waiting_for_option_b)
async def process_daily_opt_b(message: Message, state: FSMContext):
    await state.update_data(option_b=message.text.strip())
    await state.set_state(AdminAddDailyQuestionStates.waiting_for_option_c)
    await message.answer("<b>C</b> variantini kiriting:", reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminAddDailyQuestionStates.waiting_for_option_c)
async def process_daily_opt_c(message: Message, state: FSMContext):
    await state.update_data(option_c=message.text.strip())
    await state.set_state(AdminAddDailyQuestionStates.waiting_for_option_d)
    await message.answer("<b>D</b> variantini kiriting:", reply_markup=get_admin_cancel_keyboard(), parse_mode="HTML")


@router.message(AdminAddDailyQuestionStates.waiting_for_option_d)
async def process_daily_opt_d(message: Message, state: FSMContext):
    await state.update_data(option_d=message.text.strip())
    await state.set_state(AdminAddDailyQuestionStates.waiting_for_correct)

    builder = InlineKeyboardBuilder()
    builder.button(text="A", callback_data="adm_daily_corr:A")
    builder.button(text="B", callback_data="adm_daily_corr:B")
    builder.button(text="C", callback_data="adm_daily_corr:C")
    builder.button(text="D", callback_data="adm_daily_corr:D")
    builder.adjust(2)

    await message.answer("Qaysi variant <b>to'g'ri javob</b> hisoblanadi?", reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(AdminAddDailyQuestionStates.waiting_for_correct, F.data.startswith("adm_daily_corr:"))
async def process_daily_correct(call: CallbackQuery, state: FSMContext):
    correct_opt = call.data.split(":")[1].upper()
    data = await state.get_data()

    await add_daily_question(
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=correct_opt,
        points=5
    )
    await state.clear()
    await call.message.edit_text(
        "✅ <b>Kunlik savol muvaffaqiyatli saqlandi!</b>",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


# ==================== BARCHAGA XABAR YUBORISH (BROADCAST) ====================

@router.callback_query(F.data == "admin:broadcast")
async def start_broadcast(call: CallbackQuery, state: FSMContext):
    """Barchaga xabar yuborishni boshlash."""
    if not is_admin(call.from_user.id):
        return

    await state.set_state(AdminBroadcastStates.waiting_for_message)
    await call.message.edit_text(
        "<b>📢 BARCHA FOYDALANUVCHILARGA XABAR YUBORISH</b>\n\n"
        "Yubormoqchi bo'lgan xabaringizni yozing (matn, rasm yoki post):\n\n"
        "<i>Bekor qilish uchun pastdagi tugmani bosing.</i>",
        reply_markup=get_admin_cancel_keyboard(),
        parse_mode="HTML"
    )
    await call.answer()


@router.message(AdminBroadcastStates.waiting_for_message)
async def execute_broadcast(message: Message, state: FSMContext, bot: Bot):
    """Xabarni barcha foydalanuvchilarga yuborish."""
    await state.clear()
    user_ids = await get_all_user_ids()

    status_msg = await message.answer(f"⏳ Xabar {len(user_ids)} ta foydalanuvchiga yuborilmoqda...")

    success = 0
    failed = 0

    for u_id in user_ids:
        try:
            if message.text:
                await bot.send_message(chat_id=u_id, text=message.text, parse_mode="HTML")
            elif message.photo:
                await bot.send_photo(chat_id=u_id, photo=message.photo[-1].file_id, caption=message.caption or "", parse_mode="HTML")
            elif message.document:
                await bot.send_document(chat_id=u_id, document=message.document.file_id, caption=message.caption or "", parse_mode="HTML")
            success += 1
            await asyncio.sleep(0.05)  # Telegram limitlariga tushmaslik uchun
        except Exception:
            failed += 1

    await status_msg.edit_text(
        f"✅ <b>Xabar yuborish yakunlandi!</b>\n\n"
        f"📤 Yuborildi: {success} ta\n"
        f"❌ Yetib bormadi (bloklagan): {failed} ta",
        reply_markup=get_admin_main_keyboard(),
        parse_mode="HTML"
    )
