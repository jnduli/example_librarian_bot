from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          RegexHandler, Filters, ConversationHandler)
import logging
from database_setup import DBWrapper
from config import token

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
 )

logger = logging.getLogger(__name__)


CHOOSE_LIB_BOOKS, LIBRARIAN, BOOKS = range(3)
db = DBWrapper()


def start(bot, update):
    logger.info('Somebody started a conversation')
    reply_keyboard = [['Librarians', 'Books']]
    update.message.reply_text(
            '''
            Hi! I'm UP bot.
            Send /cancel to stop talking to me.\n\n
            Check out the librarians or get a list of all the books
            ''',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                             one_time_keyboard=True)
            )
    return CHOOSE_LIB_BOOKS


def choose_librarian_or_books(bot, update):
    text = update.message.text
    logger.info('Chose: {}'.format(text))
    if text.lower() == 'librarians':
        #  'Print librarians'
        logger.info('In librarian thing')
        librarians(bot, update)
        return LIBRARIAN
    elif text.lower() == 'books':
        all_books(bot, update)
        return BOOKS


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def librarians(bot, update):
    logger.info('Returning list of librarians')
    librarians = db.librarians
    reply_keyboard = [[a[0] for a in librarians]]
    update.message.reply_text(
            '''
            Librarians
            ''',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                             one_time_keyboard=True)
            )


def all_books(bot, update):
    books = [book[0] + ' with ' + book[1] for book in db.books]
    text = '\n'.join(books)
    update.message.reply_text(text)


def librarian_books(bot, update):
    librarian = update.message.text
    books = db.get_librarian_books(librarian)
    reply = "Books in {}'s possession:".format(librarian)
    books = ','.join(books)
    update.message.reply_text(reply + books)


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def cancel(bot, update):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    """Start the bot."""
    logger.info("Launching librarian bot")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                CHOOSE_LIB_BOOKS: [RegexHandler(
                    '^(Librarians|Books)$', choose_librarian_or_books)],
                LIBRARIAN: [MessageHandler(Filters.text, librarian_books)],
                BOOKS: [MessageHandler(Filters.text, echo)]
                },
            fallbacks=[CommandHandler('cancel', cancel)]
            )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
