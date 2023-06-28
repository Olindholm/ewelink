import base64
import hashlib
import hmac
from aiohttp import ClientResponse, ClientSession, JsonPayload
from traceback import TracebackException
from types import TracebackType
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
            " ".join(
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
    """eWeLink API class."""

    def __init__(
        self,
        app_cred: AppCredentials,
        user_cred: EmailUserCredentials,
        client_session: Optional[ClientSession] = None,
    ) -> None:
        """Initiates a new instance.

        Initiation of this class must be done in an async function.
        """
        self._app_cred = app_cred
        self._user_cred = user_cred
        self._client_session = client_session if client_session else ClientSession()
        self._login: Optional[LoginResponse] = None

    async def __aenter__(self) -> "EWeLink":
        return self

    async def __aexit__(
        self,
        exc_type: Exception,
        exc_val: TracebackException,
        traceback: TracebackType,
    ) -> None:
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

    async def _auth_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[dict[str, str]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Makes an authenaticated (user logged in) request."""
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
                        data=EWeLinkPayload(self._user_cred.dict(by_alias=True), self._app_cred),
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
    ) -> None:
        await self._auth_request(
            "POST",
            "v2/device/thing/status",
            json={
                "type": 1,
                "id": device.deviceid,
                "params": params,
            },
        )
