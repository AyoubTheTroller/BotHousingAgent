import aiohttp

class HttpClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get(self, url: str):
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    async def close(self):
        await self.session.close()
