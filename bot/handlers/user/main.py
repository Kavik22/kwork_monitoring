from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.reply import KB_MENU

router = Router()


@router.message(Command('start'))
async def __start(msg: Message):
    await msg.answer(text="В этом ботике можно получать тендеры с kwork'а", reply_markup=KB_MENU)


@router.message()
async def deleter(msg: Message):
    await msg.delete()
