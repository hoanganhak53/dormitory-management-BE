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
    start = 2022111
    for i in range(0, 50):
        name = random_vietnamese_name()
        mssv = start + i
        user_dict = {
            "email": f"{generate_email(name, mssv)}",
            "full_name": name,
            "mssv": f"{mssv}",
            "password": "12345678",
            "user_type": 1,
            "is_valid": True,
            "is_more_info": True,
            "major": "14",
            "gender": 1,
            "batch": "64",
            "phonenumber": random_phone_number(),
            "birth": "2001-01-01"
        }
        model = UserData(**user_dict)
        await model.save()
    
    return {
        "message": "Thanh cong"
    }
    
def random_vietnamese_name():
    first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đào", "Đoàn", "Vương", "Trương", "Phan", "Tạ", "Phùng", "Quách", "Đinh", "Lâm", "Quang", "Hà", "Kiều", "Mai", "Trịnh", "Lương", "Ninh", "Quỳnh", "Tiến", "Hùng", "Nam", "Khánh", "Quyết", "Cường", "Thắng", "Bảo", "Tâm", "Thiên", "Thành", "Thiện", "Tuấn", "Việt", "Xuân"]
    middle_names = ["Văn", "Hữu", "Minh", "Ngọc", "Hoàng", "Thành", "Tuấn", "Quốc", "Thiện", "Như", "Công", "Đức", "Trí", "Đình", "Nhân", "Phương", "Thắng", "Vinh", "Nhật"]
    last_names = ["Hoàng", "Vũ", "Lê", "Sơn", "Hoàng", "Hoàng Anh", "Long", "Kiên", "Bắc", "Hùng", "Trường", "Mạnh", "Dũng", "Kiên", "Đào", "Đoàn", "Vương", "Trương", "Phan", "Tuấn Anh", "Độ", "Quách", "Đinh", "Lâm", "Quang", "Hà", "Thắng", "Hiếu", "Trịnh", "Lương", "Ninh", "Nam", "Khánh", "Quyết", "Cường", "Thắng", "Bảo", "Tâm", "Thiên", "Thành", "Thiện", "Tuấn", "Việt", "Xuân"]

    first_name = random.choice(first_names)
    middle_name = random.choice(middle_names)
    last_name = random.choice(last_names)

    return f"{first_name} {middle_name} {last_name}"

def random_phone_number():
    area_code = ["03", "05", "07", "08", "09"]
    main_digits = [str(random.randint(0, 9)) for _ in range(7)]

    area_code = random.choice(area_code)
    main_digits = "".join(main_digits)

    return f"{area_code}{main_digits}"

def generate_email(full_name, student_id):
    # Tách tên thành các phần riêng biệt
    name_parts = full_name.strip().split()
    if len(name_parts) == 2:
        first_name, last_name = name_parts
    else:
        first_name = name_parts[0]
        last_name = name_parts[-1]

    # Chuyển đổi các phần tên thành lowercase và loại bỏ các dấu cách
    first_name = first_name.lower()
    last_name = last_name.lower()
    student_id = str(student_id)

    # Tạo email
    email = f"{last_name}.{first_name}{student_id}@gmail.com"
    return email