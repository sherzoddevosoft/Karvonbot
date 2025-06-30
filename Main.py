from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
import re

# Bot configuration
TOKEN = "8039650027:AAFfTAgJNInDBvJlRB5XPi9vZem49Ft-ygE"  # Replace with your bot token
CHANNEL_ID = "@xabarnomaaa"  # Replace with your channel ID if needed

bot = Bot(token=TOKEN)
dp = Dispatcher()
user_data = {}


# State definitions
class ConsultationForm(StatesGroup):
    full_name = State()
    age = State()
    phone = State()
    allergy = State()
    complaint = State()
    since_when = State()


class ConsultationFormDoctor(StatesGroup):
    doctor_type = State()
    full_name = State()
    age = State()
    phone = State()
    complaint = State()
    since_when = State()
    more_details = State()


class ConsultationFormNurse(StatesGroup):
    nurse_service = State()
    full_name = State()
    age = State()
    phone = State()
    complaint = State()
    since_when = State()
    more_details = State()


class ConsultationFormNanny(StatesGroup):
    full_name = State()
    age = State()
    phone = State()
    details = State()


class ConsultationFormPsychologist(StatesGroup):
    full_name = State()
    age = State()
    phone = State()
    complaint = State()
    since_when = State()
    more_details = State()


# ========== UTILITY FUNCTIONS ==========
def validate_phone(phone: str) -> bool:
    """Validate phone number format (e.g., +998901234567 or 998901234567)."""
    pattern = r"^\+?998\d{9}$"
    return bool(re.match(pattern, phone.replace(" ", "")))


# ========== MAIN MENU HANDLERS ==========
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    button = [
        [types.KeyboardButton(text="🇺🇿 O'zbekcha va 🇷🇺 Русский")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(
        "Assalomu alaykum! KarvonMed loyihasi orqali xohlagan vaqtingizda tajribali hamshiralar xizmatidan foydalanishingiz mumkin! 😊 / "
        "Здравствуйте! Через наш проект KarvonMed вы можете в любое время воспользоваться услугами опытных медицинских сестёр! 😊\n\n"
        "Iltimos, tilni tanlang / Пожалуйста, выберите язык:",
        reply_markup=keyboard
    )


@dp.message(lambda message: message.text == "🇺🇿 O'zbekcha va 🇷🇺 Русский")
async def bosh_menu(message: types.Message):
    buttons = [
        [types.KeyboardButton(text="Shifokor kerak 👩🏻‍⚕️👨🏻‍⚕️ / Нужен доктор 👩🏻‍⚕️👨🏻‍⚕️"),
         types.KeyboardButton(text="Hamshira kerak 👩🏻‍⚕️ / Нужна медсестра 👩🏻‍⚕️")],
        [types.KeyboardButton(text="Konsultatsiya (onlayn) 🩺📲 / Консультация (онлайн) 🩺📲"),
         types.KeyboardButton(text="Bog'lanish 📞 / Связаться 📞")],
        [types.KeyboardButton(text="Massaj 💆‍♂️ / Массаж 💆‍♂️")],
        [types.KeyboardButton(text="Enaga 👶🍼 / Энага 👶🍼"),
         types.KeyboardButton(text="Psixolog 🧠💬 / Психолог 🧠💬")],
        [types.KeyboardButton(text="Bot bilan ulashish 📣 / Поделиться ботом 📣")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    menu_text = (
        "Quyidagi tugmalardan birini tanlang / Выберите одну из кнопок ниже:\n\n"
        "Shifokor kerak 👩🏻‍⚕️👨🏻‍⚕️ / Нужен доктор 👩🏻‍⚕️👨🏻‍⚕️ — Shifokorlar bilan tanishing / Познакомьтесь с врачами.\n\n"
        "Hamshira kerak 👩🏻‍⚕️ / Нужна медсестра 👩🏻‍⚕️ — Hamshiralar bilan tanishing / Познакомьтесь с медсёстрами.\n\n"
        "Konsultatsiya (onlayn) 🩺📲 / Консультация (онлайн) 🩺📲 — Onlayn konsultatsiyaga yoziling / Запишитесь на онлайн-консультацию.\n\n"
        "Massaj 💆‍♂️ / Массаж 💆‍♂️ — Massaj xizmatlariga buyurtma bering / Закажите услуги массажа.\n\n"
        "Enaga 👶🍼 / Энага 👶🍼 — Bolalar uchun enaga xizmatlari / Услуги няни для детей.\n\n"
        "Psixolog 🧠💬 / Психолог 🧠💬 — Psixologik yordam va maslahat / Психологическая помощь и консультации.\n\n"
        "Bog'lanish 📞 / Связаться 📞 — Biz bilan aloqaga chiqing / Свяжитесь с нами.\n\n"
        "Bot bilan ulashish 📣 / Поделиться ботом 📣 — Botni yaqinlaringizga ulashing / Поделитесь ботом с близкими!.\n\n👇👇👇👇"
    )
    await message.answer("Iltimos, kerakli xizmatni tanlang / Пожалуйста, выберите нужную услугу:", reply_markup=keyboard)
    await message.answer(menu_text, reply_markup=keyboard)


# ========== CONSULTATION FLOW ==========
@dp.message(lambda message: message.text == "Konsultatsiya (onlayn) 🩺📲 / Консультация (онлайн) 🩺📲")
async def start_consultation(message: types.Message, state: FSMContext):
    await state.set_state(ConsultationForm.full_name)
    await message.answer("1. Iltimos, ism va familiyangizni kiriting / Пожалуйста, введите ваше имя и фамилию:",
                        reply_markup=types.ReplyKeyboardRemove())


@dp.message(ConsultationForm.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 3:
        await message.answer("Iltimos, to'liq ism va familiyani kiriting! / Пожалуйста, введите полное имя и фамилию!")
        return
    await state.update_data(full_name=message.text)
    await state.set_state(ConsultationForm.age)
    await message.answer("2. Yoshinigizni kiriting (masalan: 25) / Укажите ваш возраст (например: 25):")


@dp.message(ConsultationForm.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not 0 < int(message.text) <= 120:
        await message.answer("Iltimos, haqiqiy yoshni raqamda kiriting (0-120)! / Пожалуйста, введите реальный возраст в цифрах (0-120)!")
        return
    await state.update_data(age=int(message.text))
    await state.set_state(ConsultationForm.phone)
    await message.answer("3. Telefon raqamingiz (aloqa uchun, masalan: +998901234567) / Ваш номер телефона (для связи, например: +998901234567):")


@dp.message(ConsultationForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    if not validate_phone(message.text):
        await message.answer("Iltimos, to'g'ri telefon raqamini kiriting (+998901234567)! / Пожалуйста, введите правильный номер телефона (+998901234567)!")
        return
    await state.update_data(phone=message.text)
    await state.set_state(ConsultationForm.allergy)
    await message.answer(
        "4. Qanday allergiyalaringiz bor? (Yo'q bo'lsa 'Yo'q' deb yozing) / Какие у вас есть аллергии? (Если нет, напишите 'Нет'):")


@dp.message(ConsultationForm.allergy)
async def process_allergy(message: types.Message, state: FSMContext):
    await state.update_data(allergy=message.text)
    await state.set_state(ConsultationForm.complaint)
    await message.answer("5. Asosiy shikoyatingiz nima? / Какова ваша основная жалоба?:")


@dp.message(ConsultationForm.complaint)
async def process_complaint(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 5:
        await message.answer("Iltimos, shikoyatni batafsilroq yozing! / Пожалуйста, опишите жалобу подробнее!")
        return
    await state.update_data(complaint=message.text)
    await state.set_state(ConsultationForm.since_when)
    await message.answer("6. Qachondan beri bu shikoyatlar boshlandi? / С какого времени начались эти жалобы?:")


@dp.message(ConsultationForm.since_when)
async def process_since_when(message: types.Message, state: FSMContext):
    await state.update_data(since_when=message.text)
    data = await state.get_data()

    # Response to user
    response = (
        f"📋 Ma'lumotlaringiz / Ваши данные:\n"
        f"1. Ism / Имя: {data['full_name']}\n"
        f"2. Yosh / Возраст: {data['age']}\n"
        f"3. Telefon / Телефон: {data['phone']}\n"
        f"4. Allergiya / Аллергия: {data['allergy']}\n"
        f"5. Shikoyat / Жалоба: {data['complaint']}\n"
        f"6. Qachondan / С какого времени: {data['since_when']}\n\n"
        "✅ So'rovingiz qabul qilindi! Tez orada shifokor siz bilan bog'lanadi / "
        "✅ Ваш запрос принят! Врач свяжется с вами в ближайшее время."
    )
    await message.answer(response)
    await bosh_menu(message)

    # Send to channel
    channel_message = (
        f"🆕 Yangi konsultatsiya so'rovi / Новый запрос на консультацию:\n"
        f"👤 Ism / Имя: {data['full_name']}\n"
        f"🎂 Yosh / Возраст: {data['age']}\n"
        f"📞 Telefon / Телефон: {data['phone']}\n"
        f"🌿 Allergiya / Аллергия: {data['allergy']}\n"
        f"🤒 Shikoyat / Жалоба: {data['complaint']}\n"
        f"📅 Qachondan / С какого времени: {data['since_when']}\n"
        f"🕒 Vaqt / Время: {message.date}"
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=channel_message)
    except Exception as e:
        print(f"Kanalga xabar yuborishda xato / Ошибка при отправке в канал: {e}")

    await state.clear()


# ========== DOCTOR SELECTION ==========
@dp.message(lambda message: message.text == "Shifokor kerak 👩🏻‍⚕️👨🏻‍⚕️ / Нужен доктор 👩🏻‍⚕️👨🏻‍⚕️")
async def doctor_options(message: types.Message):
    buttons = [
        [types.KeyboardButton(text="Terapevt / Терапевт")],
        [types.KeyboardButton(text="Endokrinolog / Эндокринолог"),
         types.KeyboardButton(text="Endoskopiya / Эндоскопия")],
        [types.KeyboardButton(text="Pediatr / Педиатр"),
         types.KeyboardButton(text="Urolog / Уролог")],
        [types.KeyboardButton(text="Ortga ↙️ / Назад ↙️")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Iltimos, kerakli mutaxassislikni tanlang / Пожалуйста, выберите нужную специальность:",
                        reply_markup=keyboard)


@dp.message(lambda message: message.text in [
    "Terapevt / Терапевт", "Endokrinolog / Эндокринолог", "Endoskopiya / Эндоскопия",
    "Pediatr / Педиатр", "Urolog / Уролог"
])
async def start_doctor_consultation(message: types.Message, state: FSMContext):
    await state.update_data(doctor_type=message.text)
    await state.set_state(ConsultationFormDoctor.full_name)
    await message.answer("1. Iltimos, ism va familiyangizni kiriting / Пожалуйста, введите ваше имя и фамилию:",
                        reply_markup=types.ReplyKeyboardRemove())


# ========== DOCTOR CONSULTATION FLOW ==========
@dp.message(ConsultationFormDoctor.full_name)
async def process_doctor_full_name(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 3:
        await message.answer("Iltimos, to'liq ism va familiyani kiriting! / Пожалуйста, введите полное имя и фамилию!")
        return
    await state.update_data(full_name=message.text)
    await state.set_state(ConsultationFormDoctor.age)
    await message.answer("2. Yoshinigizni kiriting (masalan: 25) / Укажите ваш возраст (например: 25):")


@dp.message(ConsultationFormDoctor.age)
async def process_doctor_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not 0 < int(message.text) <= 120:
        await message.answer("Iltimos, haqiqiy yoshni raqamda kiriting (0-120)! / Пожалуйста, введите реальный возраст в цифрах (0-120)!")
        return
    await state.update_data(age=int(message.text))
    await state.set_state(ConsultationFormDoctor.phone)
    await message.answer("3. Telefon raqamingiz (aloqa uchun, masalan: +998901234567) / Ваш номер телефона (для связи, например: +998901234567):")


@dp.message(ConsultationFormDoctor.phone)
async def process_doctor_phone(message: types.Message, state: FSMContext):
    if not validate_phone(message.text):
        await message.answer("Iltimos, to'g'ri telefon raqamini kiriting (+998901234567)! / Пожалуйста, введите правильный номер телефона (+998901234567)!")
        return
    await state.update_data(phone=message.text)
    await state.set_state(ConsultationFormDoctor.complaint)
    await message.answer("4. Asosiy shikoyatingiz nima? / Какова ваша основная жалоба?")


@dp.message(ConsultationFormDoctor.complaint)
async def process_doctor_complaint(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 5:
        await message.answer("Iltimos, shikoyatni batafsilroq yozing! / Пожалуйста, опишите жалобу подробнее!")
        return
    await state.update_data(complaint=message.text)
    await state.set_state(ConsultationFormDoctor.since_when)
    await message.answer("5. Qachondan beri bu shikoyatlar boshlandi? / С какого времени начались эти жалобы?")


@dp.message(ConsultationFormDoctor.since_when)
async def process_doctor_since_when(message: types.Message, state: FSMContext):
    await state.update_data(since_when=message.text)
    await state.set_state(ConsultationFormDoctor.more_details)
    await message.answer(
        "6. Sizni bezovta qilayotgan sog'lig'ingizdagi muammo (Batafsilroq) / Подробно опишите проблему со здоровьем, которая вас беспокоит:")


@dp.message(ConsultationFormDoctor.more_details)
async def process_doctor_more_details(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 10:
        await message.answer("Iltimos, muammoni batafsilroq yozing! / Пожалуйста, опишите проблему подробнее!")
        return
    await state.update_data(more_details=message.text)
    data = await state.get_data()

    # Response to user
    response = (
        f"📋 Ma'lumotlaringiz / Ваши данные:\n"
        f"1. Shifokor turi / Тип врача: {data['doctor_type']}\n"
        f"2. Ism / Имя: {data['full_name']}\n"
        f"3. Yosh / Возраст: {data['age']}\n"
        f"4. Telefon / Телефон: {data['phone']}\n"
        f"5. Shikoyat / Жалоба: {data['complaint']}\n"
        f"6. Qachondan / С какого времени: {data['since_when']}\n"
        f"7. Batafsil ma'lumot / Подробная информация: {data['more_details']}\n\n"
        f"✅ {data['doctor_type']} shifokoriga so'rovingiz qabul qilindi! Tez orada siz bilan bog'lanadi / "
        f"✅ Ваш запрос принят врачу {data['doctor_type']}! Врач свяжется с вами в ближайшее время."
    )
    await message.answer(response)
    await bosh_menu(message)

    # Send to channel
    channel_message = (
        f"🆕 Yangi shifokor so'rovi / Новый запрос врачу:\n"
        f"👨‍⚕️ Shifokor turi / Тип врача: {data['doctor_type']}\n"
        f"👤 Ism / Имя: {data['full_name']}\n"
        f"🎂 Yosh / Возраст: {data['age']}\n"
        f"📞 Telefon / Телефон: {data['phone']}\n"
        f"🤒 Shikoyat / Жалоба: {data['complaint']}\n"
        f"📅 Qachondan / С какого времени: {data['since_when']}\n"
        f"🌿 Muammo / Проблема: {data['more_details']}\n"
        f"🕒 Vaqt / Время: {message.date}"
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=channel_message)
    except Exception as e:
        print(f"Kanalga xabar yuborishda xato / Ошибка при отправке в канал: {e}")

    await state.clear()


# ========== NURSE OPTIONS MENU ==========
@dp.message(lambda message: message.text == "Hamshira kerak 👩🏻‍⚕️ / Нужна медсестра 👩🏻‍⚕️")
async def nurse_options(message: types.Message):
    buttons = [
        [types.KeyboardButton(text="Bemorni parvarish qilish / Уход за больными"),
         types.KeyboardButton(text="Bandaj qo'yish / Перевязки")],
        [types.KeyboardButton(text="In'ektsiya qilish / Инъекции"),
         types.KeyboardButton(text="Fizioterapiya / Физиотерапия")],
        [types.KeyboardButton(text="Ortga ↙️ / Назад ↙️")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Iltimos, kerakli hamshira xizmat turini tanlang / Пожалуйста, выберите тип услуги медсестры:",
                        reply_markup=keyboard)


# ========== MASSAGE HANDLER (MAIN MENU) ==========
@dp.message(lambda message: message.text == "Massaj 💆‍♂️ / Массаж 💆‍♂️")
async def start_massage_consultation(message: types.Message, state: FSMContext):
    await state.update_data(nurse_service="Massaj / Массаж")
    await state.set_state(ConsultationFormNurse.full_name)
    await message.answer(
        "1. Iltimos, bemorning ism va familiyasini kiriting / Пожалуйста, введите имя и фамилию пациента:",
        reply_markup=types.ReplyKeyboardRemove())


# ========== NURSE SERVICE SELECTION HANDLER ==========
@dp.message(lambda message: message.text in [
    "Bemorni parvarish qilish / Уход за больными", "Bandaj qo'yish / Перевязки",
    "In'ektsiya qilish / Инъекции", "Fizioterapiya / Физиотерапия", "Massaj / Массаж"
])
async def start_nurse_consultation(message: types.Message, state: FSMContext):
    await state.update_data(nurse_service=message.text)
    await state.set_state(ConsultationFormNurse.full_name)
    await message.answer(
        "1. Iltimos, bemorning ism va familiyasini kiriting / Пожалуйста, введите имя и фамилию пациента:",
        reply_markup=types.ReplyKeyboardRemove())


# ========== NURSE CONSULTATION FLOW ==========
@dp.message(ConsultationFormNurse.full_name)
async def process_nurse_full_name(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 3:
        await message.answer("Iltimos, to'liq ism va familiyani kiriting! / Пожалуйста, введите полное имя и фамилию!")
        return
    await state.update_data(full_name=message.text)
    await state.set_state(ConsultationFormNurse.age)
    await message.answer("2. Bemorning yoshini kiriting (masalan: 25) / Укажите возраст пациента (например: 25):")


@dp.message(ConsultationFormNurse.age)
async def process_nurse_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not 0 < int(message.text) <= 120:
        await message.answer("Iltimos, haqiqiy yoshni raqamda kiriting (0-120)! / Пожалуйста, введите реальный возраст в цифрах (0-120)!")
        return
    await state.update_data(age=int(message.text))
    await state.set_state(ConsultationFormNurse.phone)
    await message.answer("3. Telefon raqamingiz (aloqa uchun, masalan: +998901234567) / Ваш номер телефона (для связи, например: +998901234567):")


@dp.message(ConsultationFormNurse.phone)
async def process_nurse_phone(message: types.Message, state: FSMContext):
    if not validate_phone(message.text):
        await message.answer("Iltimos, to'g'ri telefon raqamini kiriting (+998901234567)! / Пожалуйста, введите правильный номер телефона (+998901234567)!")
        return
    await state.update_data(phone=message.text)
    await state.set_state(ConsultationFormNurse.complaint)
    await message.answer("4. Asosiy muammo nimada? / В чём основная проблема?")


@dp.message(ConsultationFormNurse.complaint)
async def process_nurse_complaint(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 5:
        await message.answer("Iltimos, muammoni batafsilroq yozing! / Пожалуйста, опишите проблему подробнее!")
        return
    await state.update_data(complaint=message.text)
    await state.set_state(ConsultationFormNurse.since_when)
    await message.answer("5. Qachondan beri bu muammo mavjud? / С какого времени существует эта проблема?")


@dp.message(ConsultationFormNurse.since_when)
async def process_nurse_since_when(message: types.Message, state: FSMContext):
    await state.update_data(since_when=message.text)
    await state.set_state(ConsultationFormNurse.more_details)
    await message.answer(
        "6. Qo'shimcha ma'lumotlar (Batafsilroq yozing) / Дополнительная информация (Напишите подробнее):")


@dp.message(ConsultationFormNurse.more_details)
async def process_nurse_more_details(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 10:
        await message.answer("Iltimos, qo'shimcha ma'lumotni batafsilroq yozing! / Пожалуйста, напишите дополнительную информацию подробнее!")
        return
    await state.update_data(more_details=message.text)
    data = await state.get_data()

    # Response to user
    response = (
        f"📋 Ma'lumotlaringiz / Ваши данные:\n"
        f"1. Xizmat turi / Тип услуги: {data['nurse_service']}\n"
        f"2. Bemor ismi / Имя пациента: {data['full_name']}\n"
        f"3. Yosh / Возраст: {data['age']}\n"
        f"4. Telefon / Телефон: {data['phone']}\n"
        f"5. Muammo / Проблема: {data['complaint']}\n"
        f"6. Qachondan / С какого времени: {data['since_when']}\n"
        f"7. Qo'shimcha / Дополнительно: {data['more_details']}\n\n"
        f"✅ {data['nurse_service']} xizmati uchun so'rovingiz qabul qilindi! Tez orada hamshira siz bilan bog'lanadi / "
        f"✅ Ваш запрос на услугу {data['nurse_service']} принят! Медсестра свяжется с вами в ближайшее время."
    )
    await message.answer(response)
    await bosh_menu(message)

    # Send to channel
    channel_message = (
        f"🆕 Yangi hamshira so'rovi / Новый запрос медсестре:\n"
        f"👩‍⚕️ Xizmat turi / Тип услуги: {data['nurse_service']}\n"
        f"👤 Bemor ismi / Имя пациента: {data['full_name']}\n"
        f"🎂 Yosh / Возраст: {data['age']}\n"
        f"📞 Telefon / Телефон: {data['phone']}\n"
        f"🤒 Muammo / Проблема: {data['complaint']}\n"
        f"📅 Qachondan / С какого времени: {data['since_when']}\n"
        f"📝 Qo'shimcha / Дополнительно: {data['more_details']}\n"
        f"🕒 Vaqt / Время: {message.date}"
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=channel_message)
    except Exception as e:
        print(f"Kanalga xabar yuborishda xato / Ошибка при отправке в канал: {e}")

    await state.clear()


# ========== NANNY CONSULTATION FLOW ==========
@dp.message(lambda message: message.text == "Enaga 👶🍼 / Энага 👶🍼")
async def start_nanny_consultation(message: types.Message, state: FSMContext):
    await state.set_state(ConsultationFormNanny.full_name)
    await message.answer(
        "1. Iltimos, ism va familiyangizni kiriting / Пожалуйста, введите ваше имя и фамилию:",
        reply_markup=types.ReplyKeyboardRemove())


@dp.message(ConsultationFormNanny.full_name)
async def process_nanny_full_name(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 3:
        await message.answer("Iltimos, to'liq ism va familiyani kiriting! / Пожалуйста, введите полное имя и фамилию!")
        return
    await state.update_data(full_name=message.text)
    await state.set_state(ConsultationFormNanny.age)
    await message.answer("2. Bolaning yoshini kiriting (masalan: 3) / Укажите возраст ребёнка (например: 3):")


@dp.message(ConsultationFormNanny.age)
async def process_nanny_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not 0 <= int(message.text) <= 18:
        await message.answer("Iltimos, haqiqiy yoshni raqamda kiriting (0-18)! / Пожалуйста, введите реальный возраст в цифрах (0-18)!")
        return
    await state.update_data(age=int(message.text))
    await state.set_state(ConsultationFormNanny.phone)
    await message.answer("3. Telefon raqamingiz (aloqa uchun, masalan: +998901234567) / Ваш номер телефона (для связи, например: +998901234567):")


@dp.message(ConsultationFormNanny.phone)
async def process_nanny_phone(message: types.Message, state: FSMContext):
    if not validate_phone(message.text):
        await message.answer("Iltimos, to'g'ri telefon raqamini kiriting (+998901234567)! / Пожалуйста, введите правильный номер телефона (+998901234567)!")
        return
    await state.update_data(phone=message.text)
    await state.set_state(ConsultationFormNanny.details)
    await message.answer(
        "4. Enaga xizmati uchun qo'shimcha ma'lumotlar (masalan, soatlar, maxsus talablar) / "
        "Дополнительная информация для услуги няни (например, часы, особые требования):")


@dp.message(ConsultationFormNanny.details)
async def process_nanny_details(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 10:
        await message.answer("Iltimos, qo'shimcha ma'lumotni batafsilroq yozing! / Пожалуйста, напишите дополнительную информацию подробнее!")
        return  # Stay in the same state to allow retry
    await state.update_data(details=message.text)
    data = await state.get_data()

    # Response to user
    response = (
        f"📋 Ma'lumotlaringiz / Ваши данные:\n"
        f"1. Ism / Имя: {data['full_name']}\n"
        f"2. Yosh / Возраст: {data['age']}\n"
        f"3. Telefon / Телефон: {data['phone']}\n"
        f"4. Qo'shimcha / Дополнительно: {data['details']}\n\n"
        "✅ Enaga xizmati uchun so'rovingiz qabul qilindi! Tez orada siz bilan bog'lanadi / "
        "✅ Ваш запрос на услугу няни принят! Скоро с вами свяжутся."
    )
    await message.answer(response)
    await bosh_menu(message)

    # Send to channel
    channel_message = (
        f"🆕 Yangi enaga so'rovi / Новый запрос на няню:\n"
        f"👤 Ism / Имя: {data['full_name']}\n"
        f"🎂 Yosh / Возраст: {data['age']}\n"
        f"📞 Telefon / Телефон: {data['phone']}\n"
        f"📝 Qo'shimcha / Дополнительно: {data['details']}\n"
        f"🕒 Vaqt / Время: {message.date}"
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=channel_message)
    except Exception as e:
        print(f"Kanalga xabar yuborishda xato / Ошибка при отправке в канал: {e}")

    await state.clear()
# ========== PSYCHOLOGIST CONSULTATION FLOW ==========
@dp.message(lambda message: message.text == "Psixolog 🧠💬 / Психолог 🧠💬")
async def start_psychologist_consultation(message: types.Message, state: FSMContext):
    await state.set_state(ConsultationFormPsychologist.full_name)
    await message.answer(
        "1. Iltimos, ism va familiyangizni kiriting / Пожалуйста, введите ваше имя и фамилию:",
        reply_markup=types.ReplyKeyboardRemove())


@dp.message(ConsultationFormPsychologist.full_name)
async def process_psychologist_full_name(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 3:
        await message.answer("Iltimos, to'liq ism va familiyani kiriting! / Пожалуйста, введите полное имя и фамилию!")
        return
    await state.update_data(full_name=message.text)
    await state.set_state(ConsultationFormPsychologist.age)
    await message.answer("2. Yoshinigizni kiriting (masalan: 25) / Укажите ваш возраст (например: 25):")


@dp.message(ConsultationFormPsychologist.age)
async def process_psychologist_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not 0 < int(message.text) <= 120:
        await message.answer("Iltimos, haqiqiy yoshni raqamda kiriting (0-120)! / Пожалуйста, введите реальный возраст в цифрах (0-120)!")
        return
    await state.update_data(age=int(message.text))
    await state.set_state(ConsultationFormPsychologist.phone)
    await message.answer("3. Telefon raqamingiz (aloqa uchun, masalan: +998901234567) / Ваш номер телефона (для связи, например: +998901234567):")


@dp.message(ConsultationFormPsychologist.phone)
async def process_psychologist_phone(message: types.Message, state: FSMContext):
    if not validate_phone(message.text):
        await message.answer("Iltimos, to'g'ri telefon raqamini kiriting (+998901234567)! / Пожалуйста, введите правильный номер телефона (+998901234567)!")
        return
    await state.update_data(phone=message.text)
    await state.set_state(ConsultationFormPsychologist.complaint)
    await message.answer("4. Asosiy muammo yoki shikoyatingiz nima? / В чём основная проблема или жалоба?")


@dp.message(ConsultationFormPsychologist.complaint)
async def process_psychologist_complaint(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 5:
        await message.answer("Iltimos, muammoni batafsilroq yozing! / Пожалуйста, опишите проблему подробнее!")
        return
    await state.update_data(complaint=message.text)
    await state.set_state(ConsultationFormPsychologist.since_when)
    await message.answer("5. Qachondan beri bu muammo mavjud? / С какого времени существует эта проблема?")


@dp.message(ConsultationFormPsychologist.since_when)
async def process_psychologist_since_when(message: types.Message, state: FSMContext):
    await state.update_data(since_when=message.text)
    await state.set_state(ConsultationFormPsychologist.more_details)
    await message.answer(
        "6. Qo'shimcha ma'lumotlar (masalan, muammoning tafsilotlari, nima yordam berishini xohlaysiz) / "
        "Дополнительная информация (например, детали проблемы, какую помощь вы хотите получить):")


@dp.message(ConsultationFormPsychologist.more_details)
async def process_psychologist_more_details(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 10:
        await message.answer("Iltimos, qo'shimcha ma'lumotni batafsilroq yozing! / Пожалуйста, напишите дополнительную информацию подробнее!")
        return
    await state.update_data(more_details=message.text)
    data = await state.get_data()

    # Response to user
    response = (
        f"📋 Ma'lumotlaringiz / Ваши данные:\n"
        f"1. Ism / Имя: {data['full_name']}\n"
        f"2. Yosh / Возраст: {data['age']}\n"
        f"3. Telefon / Телефон: {data['phone']}\n"
        f"4. Muammo / Проблема: {data['complaint']}\n"
        f"5. Qachondan / С какого времени: {data['since_when']}\n"
        f"6. Qo'shimcha / Дополнительно: {data['more_details']}\n\n"
        "✅ Psixolog xizmati uchun so'rovingiz qabul qilindi! Tez orada siz bilan bog'lanadi / "
        "✅ Ваш запрос на услугу психолога принят! Скоро с вами свяжутся."
    )
    await message.answer(response)
    await bosh_menu(message)

    # Send to channel
    channel_message = (
        f"🆕 Yangi psixolog so'rovi / Новый запрос психологу:\n"
        f"👤 Ism / Имя: {data['full_name']}\n"
        f"🎂 Yosh / Возраст: {data['age']}\n"
        f"📞 Telefon / Телефон: {data['phone']}\n"
        f"🤒 Muammo / Проблема: {data['complaint']}\n"
        f"📅 Qachondan / С какого времени: {data['since_when']}\n"
        f"📝 Qo'shimcha / Дополнительно: {data['more_details']}\n"
        f"🕒 Vaqt / Время: {message.date}"
    )
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=channel_message)
    except Exception as e:
        print(f"Kanalga xabar yuborishda xato / Ошибка при отправке в канал: {e}")

    await state.clear()


# ========== CONTACT OPTIONS ==========
@dp.message(lambda message: message.text == "Bog'lanish 📞 / Связаться 📞")
async def contact(message: types.Message):
    buttons = [
        [types.KeyboardButton(text="Telegram 📨"),
         types.KeyboardButton(text="Instagram 📸")],
        [types.KeyboardButton(text="Ortga ↙️ / Назад ↙️")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Biz bilan bog'lanish uchun / Для связи с нами:", reply_markup=keyboard)


@dp.message(lambda message: message.text == "Telegram 📨")
async def tginfo(message: types.Message):
    await message.answer("Telegram: https://t.me/Tolibjon_Ubaydullayev")


@dp.message(lambda message: message.text == "Instagram 📸")
async def instainfo(message: types.Message):
    await message.answer("Instagram: https://www.instagram.com/devosoft.uz/")


# ========== SHARE BOT ==========
@dp.message(lambda message: message.text == "Bot bilan ulashish 📣 / Поделиться ботом 📣")
async def share_bot(message: types.Message):
    bot_link = f"https://t.me/{(await bot.get_me()).username}"
    await message.answer(
        f"Do'stlaringizga botimizni ulashing! 😊 / Поделитесь нашим ботом с друзьями! 😊\n{bot_link}",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="Ortga ↙️ / Назад ↙️")]], resize_keyboard=True))


# ========== BACK BUTTONS ==========
@dp.message(lambda message: message.text == "Ortga ↙️ / Назад ↙️")
async def back_to_menu(message: types.Message):
    await bosh_menu(message)


# ========== MAIN FUNCTION ==========
async def main():
    print('Bot ishga tushdi / Бот запущен...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())