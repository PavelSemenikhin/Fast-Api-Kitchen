from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.users import UserCreateSchema, UserLoginSchema
from services.auth import hash_password, verify_password


async def create_user(user_data: UserCreateSchema, db: AsyncSession) -> User | None:

    stmt = await db.execute(
        select(User).where(User.email == user_data.email),
    )
    result = stmt.scalar_one_or_none()
    if result:
        return None

    hashed = hash_password(user_data.password)

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(
    user_data: UserLoginSchema, db: AsyncSession
) -> User | None:
    stmt = await db.execute(
        select(User).where(User.username == user_data.username),
    )
    user = stmt.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(
        plain_password=user_data.password, hashed_password=user.hashed_password
    ):
        return None
    return user
