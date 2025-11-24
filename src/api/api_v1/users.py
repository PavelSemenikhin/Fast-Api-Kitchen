from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from core.models.db_helper import async_get_db
from core.schemas.users import UserRead, UserCreate
from crud.users import get_all_users, create_user

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(async_get_db)):
    users = await get_all_users(db=db)
    return users


@router.post(
    "/create_user/", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
async def register(user_create: UserCreate, db: AsyncSession = Depends(async_get_db)):
    user = await create_user(db=db, user_create=user_create)
    return user
