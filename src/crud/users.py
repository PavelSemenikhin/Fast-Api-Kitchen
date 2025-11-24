from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.users import UserCreate


async def get_all_users(
    db: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await db.execute(stmt)
    users = result.scalars().all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found",
        )

    return users


async def create_user(
    db: AsyncSession,
    user_create: UserCreate,
) -> User:

    user = User(
        username=user_create.username,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user
