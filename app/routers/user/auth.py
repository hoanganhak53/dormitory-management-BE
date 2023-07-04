from fastapi import APIRouter, Query
from app.dto.common import (BaseResponse, BaseResponseData)
from app.dto.user_dto import (UserRegisterRequest, UserLoginRequest, ForgotPasswordRequest)
from app.services.user_service import UserService
from app.helpers.jwt_helpers import generate_token
from app.models.user import UserData
import random
import string

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
    
    token = generate_token({"user_id": str(user_data['id'])})
    return {
        "message": "Đăng nhập thành công",
        "data": user_data,
        "token": token
    }
    
@route.get("/overview")
async def overview_ktx():
    overview = await UserService().overview()
    
    return overview


@route.post("/reset_password")
async def reset_password(input_pass: ForgotPasswordRequest):
    user = await UserData.find_one({"email": input_pass.email, "mssv": input_pass.mssv})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Email hoặc mã số sinh viên không tồn tại')
    
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(10))
    
    await user.update(
        { "$set":
            {
                "password": password
            }
        }
    )
    return {
        "message": "Mật khẩu mới đã được gửi về email của bạn",
        "new_password": password
    }


@route.get("/gen")
async def gen_ktx():
    for i in range(0, 30):
        user_dict = {
            "email": f"example{i}@gmail.com",
            "full_name": f"Nguyen Van A {i}",
            "mssv": f"2019011{i}",
            "password": "12345678",
            "user_type": 1,
            "is_valid": True,
            "is_more_info": True,
            "major": "14",
            "gender": 1,
            "batch": "64",
            "phonenumber": f"{i}12345{i}003",
            "birth": "2001-01-01"
        }
        model = UserData(**user_dict)
        await model.save()
    
    return {
        "message": "Thanh cong"
    }