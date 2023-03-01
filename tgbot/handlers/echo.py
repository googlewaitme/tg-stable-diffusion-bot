from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.services.stable_diffusion import StableDiffusion
from tgbot.models.generation_stat import Generation

from googletrans import Translator
import datetime


async def bot_echo(message: types.Message, current_user):
    await message.answer('Генерация картинки началась⌛')
    repl_token = message.bot['config'].replicate.token
    sd = StableDiffusion(repl_token)
    translator = Translator()
    output = translator.translate(message.text, dest='en')
    url = await sd.get_image_by_url(output.text)

    db_session_factory = message.bot.get('db')
    session = db_session_factory()
    generation = Generation(
        prompt_text=message.text,
        generation_time=0,  # TODO this parameter
        time_created=datetime.datetime.now(),
        user_id=current_user.id,
        user=current_user
    )
    session.add(generation)
    session.commit()
    await message.answer_photo(url)


async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Эхо в состоянии {hcode(state_name)}',
        'Содержание сообщения:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
