#!/usr/bin/env python

from setuptools import setup

setup(
    name="00-api",
    version="0.0.0",
    description="",
    author="Mikela Clemmons",
    author_email="glassresistor@gmail.com",
    url="",
    packages=["zerozero"],
    license_files=("LICENSE", "LICENSE.CNPLv7.md", "LICENSE.proprietary.md"),
    include_package_data=True,
    install_requires=[
        "Django>=3.2.9",
        "djangorestframework>=3.12.4",
        "djangorestframework-csv~=2.1.1",
        "pyyaml~=6.0",
        "celery~=5.2.3",
        "00-pilot @ git+https://gitlab.com/frame-00/00-pilot-snake.git",
    ],
    extras_require={
        "dev": [
            "tox-conda",
            "factory-boy==3.2.1",
            "pytest~=6.2.5",
            "pytest-django~=4.4.0",
            "pytest-cov~=3.0.0",
            "pytest-randomly~=3.10.2",
            "pytest-repeat~=0.9.1",
            "click~=8.0.3",
            "black~=21.11b1",
        ]
    },
)
