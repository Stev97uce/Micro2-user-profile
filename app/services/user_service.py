from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.database import database
from sqlalchemy import insert, update, select
import httpx

async def create_credentials(email: str, password: str):
    url = "http://<AUTH_SERVICE_PUBLIC_IP>:8000/credentials"
    payload = {"email": email, "password": password}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Auth service error: {response.status_code} - {response.text}")

async def register_user(user_data: UserCreate):

    await create_credentials(user_data.email, user_data.password)

    query = insert(User).values(
        email=user_data.email,
        full_name=user_data.full_name,
        phone=user_data.phone,
        address=user_data.address
    ).returning(User)

    return await database.fetch_one(query)

async def get_user_by_email(email: str):
    query = select(User).where(User.email == email)
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
