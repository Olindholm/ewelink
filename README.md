# eWeLink
An unoffical python package for the
[eWeLink API (CoolKit Open Platform)](https://coolkit-technologies.github.io/eWeLink-API/#/en/PlatformOverview).


# Overview
This python package aims to make it easy to control your IoT's. Inspired by the
[JavaScript ewelink-api package](https://github.com/skydiver/ewelink-api).

## Installation
Install using pip from the [PyPi ewelink project](https://pypi.org/project/ewelink/).
```sh
pip install ewelink
```

## Usage
In order to use the api you need two types of credentials:
1. App credentials
1. User credentials
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

        # Make API calls
        ...


if __name__ == "__main__":
    asyncio.run(main())
```


# Contributing
...


# License
This project is licensed under the [GNU General Public License v3](./LICENSE.md)
