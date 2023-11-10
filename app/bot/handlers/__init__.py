from aiogram import Router
from aiogram.filters import JOIN_TRANSITION, ChatMemberUpdatedFilter

from app.bot.handlers.user_join import user_join

router = Router(name=__name__)

router.chat_member.register(user_join, ChatMemberUpdatedFilter(JOIN_TRANSITION))


