# eWeLink
An unoffical python package for the
[eWeLink API (CoolKit Open Platform)](https://coolkit-technologies.github.io/eWeLink-API/#/en/PlatformOverview).


# Overview
This python package aims to make it easy to control your IoT's. Inspired by the
[JavaScript ewelink-api package](https://github.com/skydiver/ewelink-api).

This package is not complete, and it may also be worth checking out other alternatives,
such as:
- [SonoffLAN](https://github.com/AlexxIT/SonoffLAN)
- [and more...](https://pypi.org/search/?q=ewelink)

## Installation
Install using pip from the [PyPi ewelink project](https://pypi.org/project/ewelink/).
```sh
pip install ewelink
```

## Usage
In order to use the api you need two types of credentials:
1. **App Credentials**, which you recieve when becoming a enterprise or personal developer. You can
   read more about it at the CoolKit Open Platform [Piricing](https://coolkit-technologies.github.io/eWeLink-API/#/en/Pricing) and
   [Requirements of Calling Interface (Important):](https://coolkit-technologies.github.io/eWeLink-API/#/en/APICenterV2?id=requirements-of-calling-interface-important).
   It can be good to read the requirements, as it also mentions number of requests per second to not
   get your **app credentials** revoked.

   However, if you **JUST WANT TO GET STARTED**, you can try "borrowing" app credentials from other
   repositories, such as:
   - [skydiver/ewelink-api](https://github.com/skydiver/ewelink-api/blob/c11b3a8ab706cabcb592b4f9799314405788b640/src/data/constants.js#L1)
   - [AlexxIT/SonoffLAN](https://github.com/AlexxIT/SonoffLAN/blob/8182a153312a35f57800f18d8472806c97e02aa9/custom_components/sonoff/core/ewelink/cloud.py#L43)

1. **User Credentials**, is the credentials you use to log into your
   [eWeLink Account](https://web.ewelink.cc/).

Once you have that, you're ready to get started. Here's a small demo application showing
the basics of how to use it.
```python
import asyncio

from ewelink import EWeLink
from ewelink.types import AppCredentials, EmailUserCredentials

APP_CREDENTIALS = AppCredentials(id=..., secret=...)


async def main() -> None:
    async with EWeLink(
        APP_CREDENTIALS,
        EmailUserCredentials(email=..., password=...),
    ) as ewelink:
        # Attempt login (not needed, any call needing to login will do so automatically)
        await ewelink.login()

        # Make more API calls
        ...


if __name__ == "__main__":
    asyncio.run(main())
```


# Contributing
...


# License
This project is licensed under the [GNU General Public License v3](LICENSE.md)
