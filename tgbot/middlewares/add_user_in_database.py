from typing import Callable, Dict, Awaitable, Any

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from tgbot.models.user import User


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class AddUserInDBMiddleware(BaseMiddleware):
    async def on_process_message(
            self, message: Message, data: Dict[str, Any]) -> Any:
        user_id = message.from_user.id
        username = message.from_user.username
        db_session_factory = message.bot.get('db')
        session = db_session_factory()
        current_user = get_or_create(
            session, User, telegram_id=user_id, name=username)
        session.commit()
        data['current_user'] = current_user
