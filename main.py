import os
from io import BytesIO

import qrcode

from aiogram import Bot, Dispatcher, executor, types
from PIL import Image, ImageFont, ImageDraw

# создание новой картинки
new_img = '/new_img'

# Константы
START_MESSAGE = 'Привет, \n' \
                'я создам для тебя табличку под стекло автомобиля, с QR кодом твоего телефона. Пример таблички:'
HELP_MESSAGE = f' Для создания таблички введите свой номер телефона, \n ' \
               'он должен быть в формате 79101234567 \n '
WRONG_PHONE_MESSAGE = f'Вы написали не телефон \n ' \
                      f'телефон должен быть в формате 79101234567 \n ' \
                      f'и в нем должно быть 11 цифр'
GOOD_PHONE_MESSAGE = f'Я сгенерировал для тебя QR код с твоим телефоном: '

SIZE_X = 600
SIZE_Y = 300

# Объект бота
bot = Bot(token=os.environ['TG_API'])
# Диспетчер для бота
dp = Dispatcher(bot)


# генерируем QR код по номеру телефона
def make_qr(text):
    b = BytesIO()
    img = qrcode.make(text)
    img = img.resize((210, 210), Image.BICUBIC)
    img.save(b, format="jpeg")
    img = b.getbuffer()
    img = Image.open(BytesIO(img))
    return img


# создаем картинку под стекло с телефоном и QR кодом
def create_image(text):
    # генерируем QR
    qr = make_qr(text)
    # создем новую картинку с указанными размерами, белым цветом
    img = Image.new('RGB', (SIZE_X, SIZE_Y), (255, 255, 255, 1))
    draw = ImageDraw.Draw(img)

    # Щрифт для заголовка 1
    font_h = ImageFont.truetype("font/ChareInk-Regular.ttf", size=36)
    # Щрифт для текста 2
    font_h2 = ImageFont.truetype("font/ChareInk-Regular.ttf", size=30)

    # Рисуем границу для картинки
    draw.rectangle([0, 0, SIZE_X - 1, SIZE_Y - 1], fill='#FFFFFF', outline='#000000', width=1)

    # Выводим 4 текста на холст
    draw.text(
        (70, 30),
        'Моя машина вам мешает?',
        fill=('#1C0606'
              ),
        font=font_h,
    )
    draw.text(
        (220, 90),
        'позвоните:',
        fill=('#1C0606'
              ),
        font=font_h2,
    )
    draw.text(
        (218, 160),
        'тел:',
        fill=('#1C0606'
              ),
        font=font_h2,
    )
    draw.text(
        (275, 158),
        f'{phone_format(text)}',
        fill=('#1C0606'
              ),
        font=font_h,
    )

    # Выводим на холст сгенерированный QR
    h, w = qr.size
    x = 10
    y = 70
    img.paste(qr, (x, y, h + x, w + y))

    b = BytesIO()
    # Сохраняем итоговую картинку в буфер
    img.save(b, format="jpeg")
    img = b.getbuffer()

    return img


# Проверям, является ли текст телефоном
def is_phone(phone):
    # Удалим из строки пробелы и спец символы, характерные для записи телефона
    phone = phone.replace(" ", '').replace("-", '').replace("(", '').replace(")", '')
    # В итоге у нас должно остаться только 11 цифр
    if phone.isdigit() and len(phone) == 11:
        # Если телефон начинается с 8, то меняем ее на 7
        if phone[0] == '8':
            phone = f'7{phone[1:]}'
        return phone
    # Если строка не удовляетворяет условия выше, то она не явлеятся телефоном
    else:
        return False


# Оботражает телефон в привычном формате
def phone_format(phone):
    return f' {phone[0]} ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:12]}'


# Приветственное сообщение или сообщение help для пользователей
@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    await message.answer(text=START_MESSAGE)
    await message.answer_photo(photo=create_image('79991234567'))
    await message.answer(text=HELP_MESSAGE)


# Ожидаем введеную пользователем текстовую информацию
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def user_phone(message: types.Message):
    # Предполагаем что введеная информация телефон и проверяем
    phone = is_phone(message.text)
    if phone:
        await message.answer(text=f'{GOOD_PHONE_MESSAGE}{phone}')
        await message.answer_photo(photo=create_image(phone))
    else:
        await message.answer(text=WRONG_PHONE_MESSAGE)


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
