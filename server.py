import json
import re
from random import shuffle

import peewee
import telebot

from bot import bot
from models import User, WordTranslate, Word, Translate

pattern = re.compile(r'/add[\s]([\w]+)[\s]([\w]+)')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "/add слово перевод | Добавляет слово\n/test запрашивает слово\n")


@bot.message_handler(commands=['add'])
def add_word(message):
    user, _ = User.get_or_create(
        external_id=message.from_user.id, chat_id=message.chat.id
    )
    try:
        txt = message.text
        result = pattern.match(txt)
        raw_word, raw_translate = tuple(i.lower() for i in result.groups())
    except Exception:
        bot.reply_to(message, f'❗️ Некорректный ввод команды')
        return
    word, _ = Word.get_or_create(word=raw_word, user=user)
    translate, _ = Translate.get_or_create(translate=raw_translate, user=user)
    WordTranslate.get_or_create(word=word, translate=translate, user=user)
    bot.reply_to(message, f'🆕 Добавлено слово "{raw_word}" с переводом "{raw_translate}"')


@bot.message_handler(commands=['test'])
def get_test(message, user=None):
    user = user or User.get(User.external_id == message.from_user.id)
    pairs = WordTranslate.select()\
        .where(WordTranslate.user == user)\
        .order_by(peewee.fn.Random())\
        .limit(4)
    markup = telebot.types.InlineKeyboardMarkup()
    buttons = []
    answer = None
    for row in pairs:
        word = Word.get(Word.id == row.word.id, Word.user == row.user)
        if answer is None:
            answer = word
        translate = Translate.get(Translate.id == row.translate.id, Translate.user == row.user)
        btn = telebot.types.InlineKeyboardButton(
            text=f'{row.translate.translate}',
            callback_data=json.dumps(
                {"t": "a", "q": answer.id, "a": translate.id}
            )
        )
        buttons.append(btn)
    shuffle(buttons)
    markup.add(*buttons[:2])
    markup.add(*buttons[2:])
    bot.send_message(user.chat_id, f"❔ Слово {answer.word}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user = User.get(User.external_id == call.from_user.id)
    if call.message:
        msg = json.loads(call.data)
        if msg["t"] == "a":
            markup = telebot.types.InlineKeyboardMarkup()
            btn = telebot.types.InlineKeyboardButton(
                text=f'Еще?', callback_data=json.dumps({"t": "m"})
            )
            markup.add(btn)
            wt: WordTranslate = WordTranslate\
                .get(WordTranslate.word_id == msg["q"],
                     WordTranslate.user == user,
                     WordTranslate.translate_id == msg['a'])
            if wt:
                bot.send_message(call.message.chat.id, f"✅ Правильный ответ", reply_markup=markup)
            else:
                _wt: WordTranslate = WordTranslate \
                    .get(WordTranslate.word_id == msg["q"],
                         WordTranslate.user == user)
                t = Translate.get(Translate.id == _wt.translate_id)
                bot.send_message(call.message.chat.id, f"❌ Ошибка, правильный ответ {t.translate}", reply_markup=markup)
        if msg["t"] == "m":
            get_test(call.message, user)


if __name__ == '__main__':
    bot.infinity_polling()
