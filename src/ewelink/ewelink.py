import base64
import hashlib
import hmac
import logging
from aiohttp import ClientResponse, ClientSession, JsonPayload
from typing import Any, Optional

from .types import (
    DOMAINS,
    AppCredentials,
    Device,
    EmailUserCredentials,
    LoginResponse,
    Region,
)


class EWeLinkError(Exception):
    def __init__(
        self,
        response: ClientResponse,
        error: int,
        msg: str,
        data: dict[str, Any],
    ) -> None:
        super().__init__(
            "\n".join(
                [
                    f"eWeLink API request ({response.method}) to '{response.url}' failed.",
                    f"Error ({error}): {msg}.",
                ]
            )
        )
        self.response = response
        self.error = error
        self.msg = msg
        self.data = data


class EWeLinkPayload(JsonPayload):
    ...

    def __init__(
        self,
        value: Any,
        app_cred: AppCredentials,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(value, *args, **kwargs)

        # Calculate and set Authentication Sign
        signature = base64.b64encode(
            hmac.new(
                bytes(app_cred.secret, "utf-8"),
                self._value,
                digestmod=hashlib.sha256,
            ).digest()
        ).decode("utf-8")

        self._headers["X-CK-Appid"] = app_cred.id
        self._headers["Authorization"] = f"Sign {signature}"


class EWeLink:
    def __init__(
        self,
        app_cred: AppCredentials,
        user_cred: EmailUserCredentials,
        client_session: Optional[ClientSession] = None,
    ) -> None:
        self._app_cred = app_cred
        self._user_cred = user_cred
        self._client_session = client_session if client_session else ClientSession()
        self._login: Optional[LoginResponse] = None

    async def __aenter__(self) -> "EWeLink":
        return self

    async def __aexit__(self) -> None:
        await self.close()

    async def close(self) -> None:
        await self.logout()
        await self._client_session.close()

    async def _request(
        self,
        region: Region,
        method: str,
        endpoint: str,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Makes a HTTP(S) request."""
        async with self._client_session.request(
            method,
            f"{DOMAINS[region]}/{endpoint}",
            *args,
            **kwargs,
        ) as response:
            response.raise_for_status()
            data = await response.json()

            if data["error"]:
                raise EWeLinkError(response, data["error"], data["msg"], data["data"])

        return data["data"]

    # async def _access_token(self) -> str:
    #     await self.login()

    #     if self._login is None:
    #         raise RuntimeError("User login is None after logging in.")

    #     return self._login.access_token

    async def _auth_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[dict[str, str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Makes a authenaticated (user logged in) request."""
        _login = await self.login()

        return await self._request(
            _login.region,
            method,
            endpoint,
            headers={
                **(headers if headers else {}),
                "Authorization": f"Bearer {_login.access_token}",
            },
            *args,
            **kwargs,
        )

    async def login(self, region: Region = "cn") -> LoginResponse:
        if self._login is None:
            try:
                self._login = LoginResponse.parse_obj(
                    await self._request(
                        region,
                        "POST",
                        "v2/user/login",
                        data=EWeLinkPayload(self._user_cred, self._app_cred),
                    )
                )
            except EWeLinkError as e:
                if e.error == 10004:
                    return await self.login(region=e.data["region"])
                else:
                    raise

        return self._login

    async def logout(self) -> None:
        if self._login:
            await self._auth_request(
                "DELETE",
                "v2/user/logout",
                headers={"X-CK-Appid": self._app_cred.id},
            )
            self._login = None

    async def get_thing_list(self) -> list[Device]:
        response = await self._auth_request("GET", "v2/device/thing")
        things = response["thingList"]

        items = []
        for thing in things:
            type = thing["itemType"]
            data = thing["itemData"]

            if type == 1:
                items.append(Device.parse_obj(data))
            else:
                raise NotImplementedError()

        return items

    async def update_thing_status(
        self,
        device: Device,
        params: dict[str, Any],
        new_params: bool = False,
    ) -> None:
        if new_params is False:
            new_keys = params.keys() - device.params.keys()
            if new_keys:
                logging.warning(
                    f"Ignoring new params ({new_keys}) not previously set."
                    " Setting new params may cause undefined behaviors. If this was"
                    " intentionally, set new_params=True when calling"
                    " update_thing_status(...)."
                )

            params = {k: v for k, v in params.items() if k in device.params}

        await self._auth_request(
            "POST",
            "v2/device/thing/status",
            json={
                "type": 1,
                "id": device.deviceid,
                "params": params,
            },
        )
