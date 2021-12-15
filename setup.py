#!/usr/bin/env python

from distutils.core import setup

setup(
    name="django00",
    version="0.0.0",
    description="",
    author="Mikela Clemmons",
    author_email="glassresistor@gmail.com",
    url="",
    packages=["zerozero"],
    include_package_data=True,
    install_requires=[
        "Django~=3.2.9",
        "djangorestframework~=3.12.4",
        "djangorestframework-csv==2.1.1",
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
            "black~=21.11b1",
        ]
    },
)
