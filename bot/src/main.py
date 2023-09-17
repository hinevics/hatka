import datetime

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    ConversationHandler, CallbackQueryHandler, filters, MessageHandler
)

from config import TOKEN
from flat import get_test_flat
from logger import logger
from data_worker import update_action, update_user


END = ConversationHandler.END
CHOICE_BUTTONS_ROOMS = 'choice_1', 'choice_2', 'choice_3', 'choice_4', 'choice_studio'
CHOICE_BUTTONS_PRICE = "150_200", "200_250", "250_300", "300_350", "bolee350"
AWAITING_TEXT_RESPONSE = 1


def get_keyboard(texts: list[str], callback_data: list[str]):
    """Функция для создания кнопок
    """
    keyboard = [
            [InlineKeyboardButton(t, callback_data=c) for t, c in zip(texts, callback_data)]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Стартовая функция. Возвращает кнопку для начала работы бота.
    """
    user = update.effective_chat
    context.user_data['state'] = 0
    logger.info(f'The user (username={user.username}) launched the bot')

    # update_action(
    #     data=[(user.username, 'start', datetime.datetime.now())]
    # )

    reply_markup = get_keyboard(
        texts=["Нажимай тут ➡️"],
        callback_data=["set_up_filters_get_started"]
    )

    texts = f"Привет, {user.full_name}!\
        Я бот Hatka. Я помогу найти тебе квартиру!\nНажми для старта: "

    await update.message.reply_text(
        text=texts,
        reply_markup=reply_markup)


async def set_up_filters_get_started(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция предлагает настроить фильтры или начать подбор квартир.
    """
    user_data = update.effective_chat

    query = update.callback_query
    await query.answer()

    texts = f"{user_data.username},\
        вы можете настроить фильтры или сразу начать искать квартиру."

    reply_markup = get_keyboard(
        texts=["Фильтры 📋", "Начать 🌈"],
        callback_data=["get_number_rooms", "start_flat_selection"]
    )
    bot_answer = query.edit_message_text(
        text=texts,
        reply_markup=reply_markup)

    await bot_answer


async def get_number_rooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция запрашивает число комнат.
    """
    query = update.callback_query

    await query.answer()

    texts = "*✅ 1/3.* Выберете число комнат:"

    # TODO: Переписать функцию для создания кнопок, под разный формат
    keyboard = [
        [InlineKeyboardButton(text="1️⃣", callback_data=CHOICE_BUTTONS_ROOMS[0]),
         InlineKeyboardButton(text="2️⃣", callback_data=CHOICE_BUTTONS_ROOMS[1])],
        [InlineKeyboardButton(text="3️⃣", callback_data=CHOICE_BUTTONS_ROOMS[2]),
         InlineKeyboardButton(text="4️⃣", callback_data=CHOICE_BUTTONS_ROOMS[3])],
        [InlineKeyboardButton(text="студия ", callback_data=CHOICE_BUTTONS_ROOMS[4])]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot_answer = query.edit_message_text(
            text=texts,
            reply_markup=reply_markup,
            parse_mode="Markdown"
    )

    await bot_answer


async def get_price_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаю число комнат
    query = update.callback_query
    user = update.effective_chat
    choice_nrooms = query.data

    if choice_nrooms == 'choice_1':
        context.user_data['choice_nrooms'] = '1'
    logger.info(f'The user (username={user}) choice_nrooms={choice_nrooms}')
    # TODO: логика которая записывает выбор и будет использует его для обучения

    await query.answer()

    logger.debug('Я тут 1!')
    texts = "*✅ 2/3.* Выберете подходящую сумму:"

    keyboard = [
        [InlineKeyboardButton(text="150$-200$", callback_data=CHOICE_BUTTONS_PRICE[0]),
         InlineKeyboardButton(text="200$-250$", callback_data=CHOICE_BUTTONS_PRICE[1])],
        [InlineKeyboardButton(text="250$-300$", callback_data=CHOICE_BUTTONS_PRICE[2]),
         InlineKeyboardButton(text="300$-350$", callback_data=CHOICE_BUTTONS_PRICE[3])],
        [InlineKeyboardButton(text=">350$", callback_data=CHOICE_BUTTONS_PRICE[4])]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot_answer = query.edit_message_text(
            text=texts,
            reply_markup=reply_markup,
            parse_mode="Markdown"
    )

    await bot_answer


async def get_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция для описания себя и своего желения
    """

    # Меняю статус на слушаение сообщений
    context.user_data['state'] = AWAITING_TEXT_RESPONSE

    # Получаю пределы сумм
    query = update.callback_query
    user = update.effective_chat
    choice_price = query.data
    if choice_price == '250_300':
        context.user_data['choice_price'] = "250$-300$"
    logger.info(f'The user (username={user}) choice_price={choice_price}')

    await query.answer()

    texts = "*✅ 3/3.* Расскажите о себе или про вашу квартиру:"

    keyboard = [
        [InlineKeyboardButton(text="Пропустить ⛔", callback_data="skip")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot_answer = query.edit_message_text(
                text=texts,
                reply_markup=reply_markup,
                parse_mode="Markdown"
        )

    await bot_answer


async def handle_text_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') == AWAITING_TEXT_RESPONSE:
        user_response = update.message.text
        context.user_data['user_response'] = user_response
        logger.debug(f"SAVE: {user_response}")

        context.user_data['state'] = 0
        texts = "Мы готовы начинать.\n" + \
            "Вот ваши прдварительные настройки:\n\n" + \
            f"*Комнат:* {context.user_data['choice_nrooms']}\n" + \
            f"*Цены:* {context.user_data['choice_price']}\n" + \
            f"*Описание:* {context.user_data['user_response']}\n\n" + \
            "Фильтры вы можете поправить по команде /poll"
        keyboard = [
            [InlineKeyboardButton(text="Начать 🫡", callback_data="start_flat_selection")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot_answer = update.message.reply_text(
            text=texts,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

        await bot_answer


async def skip_abount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = 0
    texts = "Мы готовы начинать. Фильтры вы можете поправить по команде /poll"
    keyboard = [
        [InlineKeyboardButton(text="Начать 🫡", callback_data="start_flat_selection")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()
    bot_answer = query.edit_message_text(
        text=texts,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    await bot_answer


async def start_flat_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_keyboard(
        texts=["👍", "👎"],
        callback_data=["like", "dislike"]
    )
    query = update.callback_query

    await query.answer()
    data = get_test_flat()
    link = f"[🔗 открыть объявление]({data['href']})"
    answer = f"*{data['title']}*\n\n{link}"

    await query.edit_message_text(
        text=answer,
        reply_markup=reply_markup, parse_mode='Markdown')

# async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Ожидается что это будет кнопка нравится.
#     TODO:
#         - нажатие вызывает новый вариант "похожей" кв
#         - сохраняет информацию что для этого пользователя кв нрав
#     """
#     user = update.effective_chat

#     logger.info(f"The user (username={user.username}) clicked the button (button=like)")

#     update_action(
#         data=[(user.username, 'like', datetime.datetime.now())]
#     )

#     reply_markup = get_keyboard(
#         texts=["👍", "👎"],
#         callback_data=["like", "dislike"]
#     )

#     query = update.callback_query

#     await query.answer()

#     data = get_test_flat()
#     link = f"[🔗 открыть объявление]({data['href']})"
#     answer = f"*{data['title']}*\n\n{link}"

#     update_user(
#         data=[(user.username, data['id'], 'like', datetime.datetime.now())]
#     )

#     await query.edit_message_text(context.user_data["last_text"], parse_mode="Markdown")

#     context.user_data["last_text"] = answer

#     await query.message.reply_text(text=answer, reply_markup=reply_markup, parse_mode="Markdown")
#     # await query.edit_message_text(
#     #     text=answer,
#     #     reply_markup=reply_markup, parse_mode='Markdown')


# async def dislike(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Ожидается что это будет кнопка ненрав.
#     TODO:
#         - помечает что данный тип квартиры не нравится
#         - отправляет новый результат с учетом "пожелания"
#         - отправляет бекенду на сохранение информации,
#             что для этого пользователя не нравятся такие квартиры
#     """
#     user = update.effective_chat

#     logger.info(f"The user (username={user.username}) clicked the button (button=dislike)")

#     update_action(
#         data=[(user.username, 'dislike', datetime.datetime.now())]
#     )

#     reply_markup = get_keyboard(
#         texts=["👍", "👎"],
#         callback_data=["like", "dislike"]
#     )

#     query = update.callback_query

#     await query.answer()

#     data = get_test_flat()
#     link = f"[🔗 открыть объявление]({data['href']})"
#     answer = f"*{data['title']}*\n\n{link}"

#     update_user(
#         data=[(user.username, data['id'], 'dislike', datetime.datetime.now())]
#     )

#     context.user_data["last_text"] = answer

#     await query.edit_message_text(
#         text=answer,
#         reply_markup=reply_markup, parse_mode='Markdown')


# async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Okay, bye.")
#     return END


# async def all_likes_flat(update: Update):
#     """Возвращает список всех квартир которые понравились пользователю.
#     TODO:
#         - Надо придумать как хранить всю эту информацию.
#     """
#     pass


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(
        CommandHandler("start", start)
    )
    app.add_handler(
        CallbackQueryHandler(set_up_filters_get_started, pattern='set_up_filters_get_started')
    )
    app.add_handler(
        CallbackQueryHandler(get_number_rooms, pattern='get_number_rooms')
    )
    app.add_handler(
        CallbackQueryHandler(start_flat_selection, pattern='start_flat_selection')
    )
    for button_name in CHOICE_BUTTONS_ROOMS:
        app.add_handler(
            CallbackQueryHandler(get_price_limit, pattern=button_name)
        )
    for button_name in CHOICE_BUTTONS_PRICE:
        app.add_handler(
            CallbackQueryHandler(get_about, pattern=button_name)
        )
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_response))
    app.add_handler(
            CallbackQueryHandler(skip_abount, pattern='skip')
        )
    app.add_handler(
            CallbackQueryHandler(start_flat_selection, pattern='start_flat_selection')
        )

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
