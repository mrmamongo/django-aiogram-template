import logging

from aiogram import Router
from aiogram.filters import (
    CommandStart,
)
from aiogram.types import Message

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start_handler(msg: Message):
    logger.info(f'Message: {msg}')
    await msg.answer("Привет! Это бот-шаблон :)")
