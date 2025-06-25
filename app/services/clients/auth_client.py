import httpx
from app.core.config import settings

async def create_credentials(email: str, password: str):
    url = f"{settings.http://34.225.179.191:8000}/credentials"
    payload = {"email": email, "password": password}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Auth service error: {response.status_code} - {response.text}")
