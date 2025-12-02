from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.auth_dependencies import get_current_user
from core.models import async_get_db, User
from core.schemas.users import (
    UserReadSchema,
    UserCreateSchema,
    UserLoginResponseSchema,
    UserLoginSchema,
    TokenRefreshResponseSchema,
    TokenRefreshRequestSchema,
)
from crud.users import create_user, authenticate_user
from services.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

router = APIRouter()


@router.post(
    "/register/",
    response_model=UserReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreateSchema,
    db: AsyncSession = Depends(async_get_db),
):
    user = await create_user(user_data=user_data, db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with this {user_data.email} already exists.",
        )

    return user


@router.post(
    "/login/",
    response_model=UserLoginResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    user_data: UserLoginSchema,
    db: AsyncSession = Depends(async_get_db),
):
    user = await authenticate_user(user_data=user_data, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return UserLoginResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh/", response_model=TokenRefreshResponseSchema)
async def refresh(data: TokenRefreshRequestSchema):

    try:
        payload = decode_refresh_token(token=data.refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token.",
        )

    new_acccess_token = create_access_token({"sub": subject})
    return TokenRefreshResponseSchema(access_token=new_acccess_token)


@router.get("/me/", response_model=UserReadSchema, status_code=status.HTTP_200_OK)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
