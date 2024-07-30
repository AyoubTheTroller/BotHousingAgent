from aiohttp import ClientSession

class HttpClient:
    def __init__(self, event_loop):
        self.session = ClientSession(loop=event_loop)

    async def get(self, url: str):
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    async def close(self):
        await self.session.close()
