from setuptools import setup, find_packages

setup(
    name="scramble_scripts",
    version="0.1.0",
    description="Shared models and logic for Scramble App",
    author="Your Name",
    packages=find_packages(include=["scripts", "scripts.*"]),
    install_requires=[
        "pymongo",
        "pydantic",
        "bson",
        "scramble-models @ git+ssh://git@github.com/JWehder/scramble-models.git",
        "selenium",
        "requests",
        "gspread",
        "dotenv"
    ],
    python_requires=">=3.8",
)