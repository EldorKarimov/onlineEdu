from decouple import config
from django.core.management import BaseCommand
import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from django.core.cache import cache

from accounts.utils import generate_code

contact_button = ReplyKeyboardMarkup(resize_keyboard=True)
contact = KeyboardButton(text="Kontakt", request_contact=True)
contact_button.add(contact)

bot = telebot.TeleBot(config('BOT_TOKEN'), parse_mode=None)

@bot.message_handler(commands=['start'])
def start(message):
    msg = f"Assalomu aleykum {message.from_user.first_name}\n\nbotga xush kelibsiz kontaktingizni yuboring⬇️"
    bot.send_message(message.chat.id, text=msg, reply_markup=contact_button)

@bot.message_handler(content_types=['contact'])
def check_contact(message):
    if message.from_user.id == message.contact.user_id:
        code = generate_code()
        msg = f"kodingiz⬇️\n{code}"
        cache.set(code, message.from_user.id, timeout=60)
        bot.reply_to(message, msg)
        bot.send_message(message.chat.id, text="kod olish uchun /login ni bosing.", reply_markup=ReplyKeyboardRemove())
    else:
        bot.reply_to(message, "Iltimos o'z kontaktingizni yuboring⬇️")

@bot.message_handler(commands=['login'])
def login(message):
    code = generate_code()
    cache.set(code, message.from_user.id, timeout=60)
    msg = f"kodingiz⬇️\n{code}"
    bot.reply_to(message, msg)

class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.polling()