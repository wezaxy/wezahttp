import asyncio
import aiohttp
import base64

class wezahttp:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def post(self, url, data=None, **kwargs):
        return await self._request("POST", url, data=data, **kwargs)

    async def get(self, url, **kwargs):
        return await self._request("GET", url, **kwargs)

    async def _request(self, method, url, **kwargs):
        proxy = kwargs.pop('proxy', None)
        verify_ssl = kwargs.pop('verify', True)
        cookies = kwargs.pop('cookies', None)
        headers = kwargs.pop('headers', None)

        async with self.session.request(method, url, proxy=proxy, verify_ssl=verify_ssl, cookies=cookies, headers=headers, **kwargs) as response:
            return await self._build_response(response)

    async def _build_response(self, response):
        text = await response.text()
        try:
            json_data = await response.json()
        except aiohttp.ContentTypeError:
            json_data = None
        
        content = await response.read()

        return wezahttpResponse(
            status=response.status,
            text=text,
            headers=response.headers,
            json=json_data,
            content=content
        )

    async def close_session(self):
        await self.session.close()

    def __del__(self):
        asyncio.ensure_future(self.close_session())

class wezahttpResponse:
    def __init__(self, status, text, headers, json=None, content=None):
        self._status_code = status
        self._text = text
        self._headers = headers
        self._json = json
        self._content = content

    def json(self):
        return self._json

    @property
    def status_code(self):
        return self._status_code

    @property
    def headers(self):
        return self._headers

    @property
    def text(self):
        return self._text

    @property
    def content(self):
        return self._content

    def base64enc(self):
        if self._content:
            return base64.b64encode(self._content).decode('utf-8')
        else:
            return None
