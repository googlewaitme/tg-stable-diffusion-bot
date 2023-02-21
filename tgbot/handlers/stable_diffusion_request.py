from aiogram import types, Dispatcher


async def bot_echo(message: types.Message):
    await message.answer()


def register_stable_diffusion(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
