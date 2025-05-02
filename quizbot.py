import os
from telegram import Update, Poll
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")

# Temporary memory to store question per user
user_question_temp = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("QuizBot से बना quiz forward करें।")

def handle_forwarded_quiz(update: Update, context: CallbackContext):
    if update.message.poll and update.message.poll.type == "quiz":
        poll = update.message.poll
        question = poll.question
        user_id = update.effective_user.id
        user_question_temp[user_id] = question

        update.message.reply_text(
            f"सवाल मिला: \"{question}\"\n"
            "कृपया बताएं: कितने ऑप्शन चाहिए? 2 / 3 / 4"
        )
    else:
        update.message.reply_text("कृपया @QuizBot से बना हुआ quiz forward करें।")

def handle_option_number(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_question_temp:
        update.message.reply_text("कृपया पहले कोई quiz forward करें।")
        return

    if text not in ["2", "3", "4"]:
        update.message.reply_text("कृपया केवल 2, 3 या 4 में से कोई संख्या भेजें।")
        return

    num = int(text)
    question = user_question_temp.pop(user_id)

    options = ["A", "B", "C", "D"][:num]
    correct_option_id = 0  # default correct option

    update.message.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=question,
        options=options,
        type=Poll.QUIZ,
        correct_option_id=correct_option_id,
        explanation="More: @quiz_smart",
        is_anonymous=False
    )

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.forwarded & Filters.poll, handle_forwarded_quiz))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_option_number))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
