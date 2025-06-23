from ariadne import QueryType
from app.services.user_service import get_user_by_id
from app.schemas.user import UserResponse

query = QueryType()

@query.field("getUserById")
async def resolve_get_user_by_id(_, info, id):
    user = await get_user_by_id(id)
    if not user:
        return None
    return dict(UserResponse.from_orm(user))
