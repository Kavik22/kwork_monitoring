from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .states import Settings
from bot.keyboards.reply import rkr, KB_MODE, KB_ALL_PAGES, KB_MENU
from .logic import get_answer
from time import sleep

router = Router()


@router.message(F.text == 'Парсить')
async def start_setting(msg: Message, state: FSMContext):
    await state.set_state(Settings.keywords)
    await msg.answer('Напишите через пробел слова по которым будут искаться тендеры', reply_markup=rkr)


@router.message(Settings.keywords)
async def set_keywords(msg: Message, state: FSMContext):
    await state.update_data(keywords=msg.text.lower().split(' '))
    await state.set_state(Settings.mode)
    text = '''Выбери режим бота:
        1) Продолжительный - бот в течение получаса каждые 5 минут присылает новые тендеры
        2) Одноразовый - происходит выгрузка всех действующих тендеров
        '''
    await msg.answer(text=text, reply_markup=KB_MODE)


@router.message(Settings.mode, F.text == 'Одноразовый')
async def set_one_time_mode(msg: Message, state: FSMContext):
    await state.update_data(mode='Одноразовый')
    await state.set_state(Settings.pages_count)
    await msg.answer('Введите количество проверяемых страниц', reply_markup=KB_ALL_PAGES)


@router.message(Settings.pages_count)
async def set_pages_count(msg: Message, state: FSMContext):
    if msg.text == 'Все' or msg.text.isdigit():
        await state.update_data(pages_count=int(msg.text))
        data = await state.get_data()
        await state.clear()
        await msg.answer('Парсер начал работу. По её завершении вы получите желаемое)')
        text, _ = get_answer(data, numbers=[])
        if text:
            await msg.answer(text=text)
            await msg.answer(text='Выгрузка завершена', reply_markup=KB_MENU)
        else:
            await msg.answer(text='Подходящих тендеров нет(((', reply_markup=KB_MENU)


@router.message(Settings.mode, F.text == 'Продолжительный')
async def set_constant_mode(msg: Message, state: FSMContext):
    await state.update_data(mode=msg.text)
    await state.update_data(pages_count=1)
    data = await state.get_data()
    await state.clear()
    await msg.answer('Парсер начал работу. Наслаждайтесь)')
    numbers = []
    for i in range(6):
        text, numbers = get_answer(data, numbers)
        if text:
            await msg.answer(text=text, reply_markup=KB_MENU)
        if i == 5:
            await msg.answer('Сеанс парсинга закончен')
            break
        sleep(300)


@router.message(Settings.mode)
async def incorrect_mode(msg: Message, state: FSMContext):
    await msg.answer('Выбирете один из двух вариантов', reply_markup=KB_MODE)
