import io
import re

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with io.open('threescale_api/__init__.py', 'rt', encoding='utf8') as f:
    VERSION = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

requirements = ['requests']

extra_requirements = {
    'dev': [
        'pytest',
        'coverage',
        'mock',
        'python-dotenv'
    ],
    'docs': ['sphinx']
}

setup(name='3scale-api',
      version=VERSION,
      description='3scale API python client',
      author='Peter Stanko',
      author_email='stanko@mail.muni.cz',
      maintainer='Peter Stanko',
      url='https://github.com/pestanko/3scale-api-python',
      packages=find_packages(exclude=("tests",)),
      long_description=long_description,
      long_description_content_type='text/markdown',
      include_package_data=True,
      install_requires=requirements,
      extras_require=extra_requirements,
      entry_points={},
      classifiers=[
          "Programming Language :: Python :: 3",
          'Programming Language :: Python :: 3.7',
          "Operating System :: OS Independent",
          "License :: OSI Approved :: Apache Software License",
          'Intended Audience :: Developers',
          'Topic :: Utilities',
      ],
      )
