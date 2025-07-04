import re
import sys

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "devel"
if sys.argv[1] == "--release-version":
    sys.argv.pop(1)
    VERSION = sys.argv.pop(1)
    assert re.match(r"[0-9]+\.[0-9]+\.[0-9]+", VERSION), "Version definition required as first arg"

requirements = ["requests", "backoff"]

extra_requirements = {"dev": ["pytest", "coverage", "python-dotenv", "responses"], "docs": ["sphinx"]}

setup(
    name="3scale-api",
    version=VERSION,
    description="3scale API python client",
    author="Peter Stanko",
    author_email="stanko@mail.muni.cz",
    maintainer="Matej Dujava",
    maintainer_email="mdujava@redhat.com",
    url="https://github.com/3scale-qe/3scale-api-python",
    packages=find_packages(exclude=("tests",)),
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extras_require=extra_requirements,
    entry_points={},
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
