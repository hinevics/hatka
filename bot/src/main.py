from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler,
    ConversationHandler, filters, CallbackQueryHandler
)

from config import TOKEN
from flat import get_test_flat

from logger import logger, error_logger


END = ConversationHandler.END


def get_keyboard(texts: list[str], callback_data: list[str]):
    keyboard = [
            [InlineKeyboardButton(t, callback_data=c) for t, c in zip(texts, callback_data)]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_chat
    logger.info(f'The user (username={user.username}) launched the bot')
    reply_markup = get_keyboard(
        texts=["Нажимай тут ➡️"],
        callback_data=["give"]
    )
    await update.message.reply_text(
        f"Привет, {user.full_name}! Я бот Hatka. Я помогу найти тебе квартиру!\nНажми для старта: ",
        reply_markup=reply_markup)


async def give(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_chat
    logger.info(f"The user (username={user.username}) clicked the button (button=give)")
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


async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ожидается что это будет кнопка нравится.
    TODO:
        - нажатие вызывает новый вариант "похожей" кв
        - сохраняет информацию что для этого пользователя кв нрав
    """
    user = update.effective_chat

    logger.info(f"The user (username={user.username}) clicked the button (button=like)")

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


async def dislike():
    """Ожидается что это будет кнопка ненрав.
    TODO:
        - помечает что данный тип квартиры не нравится
        - отправляет новый результат с учетом "пожелания"
        - отправляет бекенду на сохранение информации,
            что для этого пользователя не нравятся такие квартиры
    """
    pass


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Okay, bye.")
    return END


async def all_likes_flat():
    """Возвращает список всех квартир которые понравились пользователю.
    TODO:
        - Надо придумать как хранить всю эту информацию.
    """
    pass


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(give, pattern='give'))
    app.add_handler(CallbackQueryHandler(like, pattern='like'))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
