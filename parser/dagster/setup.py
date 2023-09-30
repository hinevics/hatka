from setuptools import find_packages, setup

setup(
    name="parser-page-readlt",
    packages=find_packages(exclude=["parser-page-readlt"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
