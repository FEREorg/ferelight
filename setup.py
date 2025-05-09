import sys
from setuptools import setup, find_packages

NAME = "ferelight"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion[swagger-ui]<3.0.0",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0",
    "setuptools>=21.0.0",
    "Flask==2.2.5",
    "psycopg2-binary==2.9.10",
    "pgvector>=0.3.6",
    "torch>=2.6.0",
    "open_clip_torch>=2.29.0",
    "transformers>=4.47.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="FERElight",
    author="FERElight Team",
    author_email="",
    url="https://github.com/FEREorg/ferelight",
    keywords=["OpenAPI", "FERElight", "feature extraction", "retrieval engine"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['ferelight=ferelight.__main__:main']},
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
