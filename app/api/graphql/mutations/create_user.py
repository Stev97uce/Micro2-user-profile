from ariadne import MutationType
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import register_user

mutation = MutationType()

@mutation.field("createUser")
async def resolve_create_user(_, info, input):
    try:
        user_data = UserCreate(**input)
        user = await register_user(user_data)
        return dict(UserResponse.from_orm(user))
    except Exception as e:
        return {"error": str(e)}

