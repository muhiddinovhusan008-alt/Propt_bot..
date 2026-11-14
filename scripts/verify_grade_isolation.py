import asyncio
from database.models import get_books_by_subject_and_grade, get_subjects

async def verify():
    subjects = await get_subjects()
    print("Grade isolation test boshlandi...")
    passed = 0
    total = 0

    for s in subjects:
        sub_id = s["id"]
        sub_name = s["name"]
        for g in range(5, 12):
            grade_str = f"{g}-sinf"
            books = await get_books_by_subject_and_grade(sub_id, grade_str)
            total += 1
            for b in books:
                # Kitobning grade qiymati aynan shu sinfga to'g'ri keladimi?
                b_grade = b["grade"]
                assert grade_str in b_grade or str(g) == b_grade or f"{g}-sinf" in b_grade, \
                    f"Xatolik! {b['title']} ({b_grade}) {grade_str} ga tushib qoldi!"
            passed += 1

    print(f"Barcha {total} ta sinf-fan kombinatsiyasi tekshirildi! Barchasi o'zaro izolyatsiyalangan va to'g'ri ishlamoqda ({passed}/{total}).")

if __name__ == "__main__":
    asyncio.run(verify())
