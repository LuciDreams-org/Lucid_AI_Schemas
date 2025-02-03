"""Python setup.py for lucid_ai_schemas package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("lucid_ai_schemas", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="lucid_ai_schemas",
    version=read("lucid_ai_schemas", "VERSION"),
    description="Awesome lucid_ai_schemas created by LuciDreams-org",
    url="https://github.com/LuciDreams-org/Lucid_AI_Schemas/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="LuciDreams-org",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["lucid_ai_schemas = lucid_ai_schemas.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
