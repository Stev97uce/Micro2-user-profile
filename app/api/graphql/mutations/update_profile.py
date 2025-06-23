from ariadne import MutationType
from app.schemas.user import UserUpdate, UserResponse
from app.services.user_service import update_user

mutation = MutationType()

@mutation.field("updateProfile")
async def resolve_update_profile(_, info, id, input):
    try:
        update_data = UserUpdate(**input)
        updated_user = await update_user(id, update_data)
        return dict(UserResponse.from_orm(updated_user))
    except Exception as e:
        return {"error": str(e)}
