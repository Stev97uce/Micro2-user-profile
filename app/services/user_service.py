from app.schemas.user import UserCreate
from app.models.user import User
from app.core.database import database
from sqlalchemy import insert
from app.services.clients.auth_client import create_credentials
from sqlalchemy import update, select
from app.schemas.user import UserUpdate
from sqlalchemy import select
from app.models.user import User

async def register_user(user_data: UserCreate):
    # 1. Crear credenciales en auth-service
    await create_credentials(user_data.email, user_data.password)

    # 2. Insertar perfil en base de datos
    query = insert(User).values(
        email=user_data.email,
        full_name=user_data.full_name,
        phone=user_data.phone,
        address=user_data.address
    ).returning(User)

    return await database.fetch_one(query)

async def update_user(user_id: int, update_data: UserUpdate):
    values = update_data.dict(exclude_unset=True)

    query = (
        update(User)
        .where(User.id == user_id)
        .values(**values)
        .returning(User)
    )

    return await database.fetch_one(query)

async def get_user_by_id(user_id: int):
    query = select(User).where(User.id == user_id)
    return await database.fetch_one(query)
