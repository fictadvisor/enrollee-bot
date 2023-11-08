from aiogram.types import ChatMemberUpdated

from app.messages.group import GREATING_MESSAGE


async def user_join(event: ChatMemberUpdated) -> None:
    await event.answer(await GREATING_MESSAGE.render_async(user=event.new_chat_member.user))
