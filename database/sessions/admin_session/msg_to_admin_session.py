from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MsgToAdministration

async def orm_add_user_msg(session: AsyncSession,
                           user_id: int,
                           username: str,
                           msg_id: int) -> None:
    session.add(MsgToAdministration(
        user_id = user_id,
        username = username,
        msg_id = msg_id
    ))
    await session.commit()