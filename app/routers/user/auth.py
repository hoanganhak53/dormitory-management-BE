from fastapi import APIRouter, Query
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.user_dto import (UserRegisterRequest, UserLoginRequest, LoginDataResponse)
from app.services.user_service import UserService
from app.helpers.jwt_helpers import generate_token

route = APIRouter(tags=['Auth'], prefix="/auth")


@route.post("/register")
async def register(register_input: UserRegisterRequest):
    user_id = await UserService().register(register_input)
    
    return BaseResponseData(
        message="Tạo tài khoản thành công",
        data=user_id
    )


@route.post("/login")
async def login(login_input: UserLoginRequest):
    user_data = await UserService().login(login_input)
    
    token = await generate_token(str(user_data.id))
    return LoginDataResponse(
        message="Đăng nhập thành công",
        data=user_data,
        token=token
    )