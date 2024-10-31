import httpx
import asyncio
import random

async def request(client: httpx.AsyncClient):
    response = await client.post("https://www.rivestsoft.com/nickname/getRandomNickname.ajax")
    return response

async def getNickname():
    async with httpx.AsyncClient() as client:
        
        req = [request(client)]
        result = await asyncio.gather(*req)

        res_dict = result[0].json()

        randN = random.randint(100, 999)

        return res_dict['data'] + str(randN)
