"""
Telegram bot for professional retraining group
"""
from configparser import ConfigParser

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from schedule import Schedule


config = ConfigParser()
config.read("config.ini")

TOKEN = config["SECRET"]["token"]
LIMIT = int(config["DEFAULT"]["limit"])
LIBRARY = config["DEFAULT"]["library"]
REPO = config["DEFAULT"]["repo"]


async def schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles schedule
    """
    schedule = Schedule()
    try:
        lectures = schedule.get(LIMIT)
        await update.message.reply_text(lectures)

    except:

        await update.message.reply_text(
            "Невозможно получить расписание"
        )
        return


async def room_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles room
    """
    schedule = Schedule()
    try:
        room = schedule.get_room()
        await update.message.reply_text(room)

    except:

        await update.message.reply_text(
            "Ошибка при получении аудитории"
        )
        return


async def repo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    returns repo link
    """

    await update.message.reply_text(REPO)


async def lib_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    returns library link
    """
    await update.message.reply_text(LIBRARY)

async def help_handler(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = f"/room - возвращает аудиторию, в которой, пройдет следующее занятие\n" \
          f"/sch, /schedule - возвращает расписание {LIMIT} следующих занятий\n" \
          f"/repo - вовращает ссылку на репозиторий, если вдруг охота подредактировать бота\n" \
          f"/lib - возвращает ссылку на небольшую коллекцию литературы\n" \
          f"\n" \
          f"Расписание берется со странички онлайн группы, пока занятия у нас совпадают, " \
          f"аудитория - со странички очной группы"
    await update.message.reply_text(msg)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler(["schedule", "sch"], schedule_handler))
    app.add_handler(CommandHandler("room", room_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("repo", repo_handler))
    app.add_handler(CommandHandler("lib", lib_handler))

    app.run_polling()


if __name__ == "__main__":
    main()


