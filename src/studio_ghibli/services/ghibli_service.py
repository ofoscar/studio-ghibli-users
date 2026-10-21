import httpx
from fastapi import HTTPException

from studio_ghibli.schemas.ghibli import GhibliResource

BASE_URL = "https://ghibliapi.vercel.app"

async def fetch_ghibli_data(
    client: httpx.AsyncClient,
    resource: GhibliResource,
    item_id: str | None = None,
):
  url = f"{BASE_URL}/{resource.value}"

  if item_id is not None:
    url = f"{url}/{item_id}"

  try: 
    response = await client.get(url)

  except httpx.TimeoutException:
    raise HTTPException(status_code=504, detail="Ghibli API timed out")
  except httpx.RequestError:
    raise HTTPException(status_code=502, detail="Could not reach Ghibli API")

  if response.status_code == 404:
    raise HTTPException(status_code=404, detail="Ghibli item not found")

  if response.is_error:
    raise HTTPException(status_code=502, detail="Ghibli API returned an error")

  return response.json()