from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler,
    ConversationHandler, filters, CallbackQueryHandler
)

from config import TOKEN
from flat import get_test_flat

from logger import logger, error_logger


END = ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_chat
    logger.info(f'The user {user_name.username} launched the bot')
    keyboard = [
            [InlineKeyboardButton("Нажимай тут ➡️", callback_data="give")]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я бот Hatka. Я помогу найти тебе квартиру!\nНажми для старта: ",
        reply_markup=reply_markup)


async def give(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
            [InlineKeyboardButton("👍", callback_data="like"),
             InlineKeyboardButton("👎", callback_data="dislike")]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()

    data = get_test_flat()
    link = f"[🔗 открыть объявление]({data['href']})"
    answer = f"*{data['title']}*\n\n{link}"

    await query.edit_message_text(
        text=answer,
        reply_markup=reply_markup, parse_mode='Markdown')


async def like():
    """Ожидается что это будет кнопка нравится.
    TODO:
        - нажатие вызывает новый вариант "похожей" кв
        - сохраняет информацию что для этого пользователя кв нрав
    """


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
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
