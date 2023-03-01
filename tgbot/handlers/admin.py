from aiogram import Dispatcher
from aiogram.types import Message

from datetime import date, datetime, timedelta


from tgbot.models.user import User
from tgbot.models.generation_stat import Generation


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


async def send_statistic(message: Message):
    # /stats 01-01-2023 01-03-2023 -> [01-01-2023 01-03-2023)
    # /stats -> [today, today)
    # /stats 01-01-2023 -> [01-01-2023, today)
    array = message.text.strip().split()

    date_template = "%d-%m-%Y"
    addition_for_end_day = timedelta(days=1) - timedelta(microseconds=1)
    today_string = date.today().strftime(date_template)
    array.append(today_string)
    array.append(today_string)
    start_str, end_str = array[1], array[2]

    try:
        start = datetime.strptime(start_str, date_template)
        end = datetime.strptime(end_str, date_template)
        end = end + addition_for_end_day
    except ValueError:
        await message.answer('Сообщения в формате /stats 01-01-2023 01-03-2023')

    db_session_factory = message.bot.get('db')
    session = db_session_factory()

    new_users_in_period = session.query(User).filter(
        User.time_created >= start,
        User.time_created <= end).count()

    new_generations_in_period = session.query(Generation).filter(
        Generation.time_created >= start,
        Generation.time_created <= end).count()

    text_array = [
        f"{start_str} {end_str}",
        f"Новых пользователей за период: {new_users_in_period}",
        f"Новые генерации за период: {new_generations_in_period}"
    ]
    await message.answer("\n".join(text_array))


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(send_statistic, commands=["stats"], state="*", is_admin=True)
