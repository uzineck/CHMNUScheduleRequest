import os
from dataclasses import dataclass
from typing import Any

import aiohttp

from core.constants import APP, ROUTER
from core.json_handler import JsonHandler


@dataclass
class CHMNUScheduleRequestBot:
    protocol: str
    domain: str
    api_version: str
    json_converter: JsonHandler = JsonHandler()
    access_token: str | None = None

    def _give_response(self, response, original_response):
        try:
            return response
        except KeyError:
            pass

    def _build_headers(self):
        headers = {}
        csrf_token = os.getenv('CSRF_TOKEN')
        if csrf_token:
            headers['X-CSRFToken'] = csrf_token
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'

        return headers

    async def _make_post_request(self, url, request_body: dict[str, Any] | None = None) -> dict[dict[str, Any]] | dict[str, Any]:
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
            headers = self._build_headers()
            session.cookie_jar.update_cookies({'csrftoken': headers['X-CSRFToken']})
            async with session.post(url=url, json=request_body, headers=headers) as response:
                response = await response.json()
                if 'detail' in response.keys():
                    print(response.get('detail'))
                return response

    async def _make_get_request(self, url) -> dict[dict[str, Any]] | dict[str, Any]:
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
            headers = self._build_headers()
            session.cookie_jar.update_cookies({'csrftoken': headers['X-CSRFToken']})
            async with session.get(url=url, headers=headers) as response:
                response = await response.json()
                if 'detail' in response.keys():
                    print(response.get('detail'))
                return response

    def build_url(
            self,
            app: str,
            router: str,
            handler: str,
            identifier: str | None = None,
            sec_identifier: str | None = None,
            query: dict | None = None,
    ) -> str:
        return (
            f"{self.protocol}://{self.domain}/api/{self.api_version}"
            f"/{app}"
            f"/{router}"
            f"{f'/{identifier}' if identifier else ''}"
            f"/{handler}"
            f"{f'/{sec_identifier}' if sec_identifier else ''}"
            f"?{'&'.join(f'{key}={value}' for key, value in query.items()) if query else ''}"
        )

    async def login(self, email: str, password: str) -> tuple[str, str]:
        url = self.build_url(app=APP.CLIENT, router=ROUTER.CLIENT, handler='log-in')
        request_body = {
            'email': email,
            'password': password
        }
        response = await self._make_post_request(url=url, request_body=request_body)
        return self._give_response(
            response=(
                response.get('data').get('access_token'),
                response.get('data').get('refresh_token')
            ),
            original_response=response,
        )

    async def update_access_token(self, refresh_token: str) -> str:
        url = self.build_url(app=APP.CLIENT, router=ROUTER.CLIENT, handler='update_access_token')
        request_body = {
            'token': refresh_token
        }
        response = await self._make_post_request(url=url, request_body=request_body)
        return self._give_response(response=response.get('data').get('access_token'), original_response=response)

    async def get_all_subjects(self) -> dict[list[dict[str, Any]], Any]:
        url = self.build_url(app=APP.SCHEDULE, router=ROUTER.SUBJECT, handler='all')

        response = await self._make_get_request(url=url)
        return self._give_response(response=response.get('data'), original_response=response)

    async def create_subject(self, subject: str):
        url = self.build_url(app=APP.SCHEDULE, router=ROUTER.SUBJECT, handler='')
        request_body = {
            'title': subject
        }
        response = await self._make_post_request(url=url, request_body=request_body)
        return self._give_response(response=response.get('data'), original_response=response)

    async def create_teacher(self, first_name: str, last_name: str, middle_name: str, rank: str):
        url = self.build_url(app=APP.SCHEDULE, router=ROUTER.TEACHER, handler='')
        request_body = {
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'rank': rank
        }
        response = await self._make_post_request(url=url, request_body=request_body)
        return self._give_response(response=response.get('data'), original_response=response)

    async def create_faculty(self, name: str, code_name: str):
        url = self.build_url(app=APP.SCHEDULE, router=ROUTER.FACULTY, handler='')
        request_body = {
            'name': name,
            'code_name': code_name
        }
        response = await self._make_post_request(url=url, request_body=request_body)
        return self._give_response(response=response.get('data'), original_response=response)