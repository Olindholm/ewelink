import os
from setuptools import setup

deps = [
    "aiohttp",
    "pydantic",
]
test_deps = ["pytest>=7", "pytest-asyncio", "pytest-cov"]
black_deps = ["black==22.8.0"]
isort_deps = ["isort==5.10.1"]
mypy_deps = ["mypy==0.991", *test_deps, "types-setuptools", "packaging", "types-PyYAML"]
flake8_deps = ["flake8==6.0.0", "flake8-pyproject>=1.2.0"]
dev_deps = ["tox", *test_deps, *black_deps, *isort_deps, *mypy_deps, *flake8_deps]

# Set build date and umask (makes wheels reprocudible)
# PEP 552: https://peps.python.org/pep-0552/
# https://github.com/pypa/wheel/issues/362
os.environ["SOURCE_DATE_EPOCH"] = "315532800"  # 1980-01-01 00:00 UTC
os.umask(0o022)

version = os.environ.get("PACKAGE_VERSION")

setup(
    # General
    name="ewelink",
    version=(version if version else "0+dev"),
    # Package data (files)
    package_data={"": ["py.typed"]},
    # Dependencies
    python_requires=">=3.9",
    install_requires=deps,
    extras_require={
        "test": test_deps,
        "black": black_deps,
        "isort": isort_deps,
        "mypy": mypy_deps,
        "flake8": flake8_deps,
        "dev": dev_deps,
    },
)
