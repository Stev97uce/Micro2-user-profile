import httpx
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate
from app.models.user import User
from app.core.database import database
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import select

async def check_user_exists(email: str):
    url = f"http://34.225.179.191:8000/check_user_exists"
    payload = {"email": email}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al verificar el usuario en auth-service: {response.status_code} - {response.text}")

async def create_credentials(email: str, password: str):
    url = "http://34.225.179.191:8000/credentials"
    payload = {"email": email, "password": password}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code == 201:
        return response.json() 
    else:
        raise Exception(f"Credenciales incorrectas o error en auth-service: {response.status_code} - {response.text}")

async def register_user(user_data: UserCreate):
    try:
        user_exists = await check_user_exists(user_data.email)
        if user_exists.get("exists", False):
            raise Exception(f"El usuario con email {user_data.email} ya existe en auth-service")

        credentials_response = await create_credentials(user_data.email, user_data.password)
        user_id = credentials_response['user_id']

        query = insert(User).values(
            email=user_data.email,
            full_name=user_data.full_name,
            phone=user_data.phone,
            address=user_data.address,
            user_id=user_id 
        ).returning(User)

        return await database.fetch_one(query)

    except Exception as e:
        await delete_user_in_auth_service(user_data.email)
        raise e

async def delete_user_in_auth_service(email: str):
    url = f"http://34.225.179.191:8000/delete_user"
    payload = {"email": email}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Error al eliminar usuario de auth-service: {response.status_code} - {response.text}")
    
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