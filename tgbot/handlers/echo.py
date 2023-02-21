from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
from tgbot.services.stable_diffusion import StableDiffusion

from googletrans import Translator


async def bot_echo(message: types.Message):
    await message.answer('Генерация картинки началась⌛')
    repl_token = message.bot['config'].replicate.token
    sd = StableDiffusion(repl_token)
    translator = Translator()
    output = translator.translate(message.text, dest='en')
    url = await sd.get_image_by_url(output.text)
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
