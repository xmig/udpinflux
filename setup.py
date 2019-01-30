#!/usr/bin/env python

try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup, find_packages

setup(
    version='1.0',

    name="udpinflux",
    namespace_packages=['udpinflux'],
    packages=find_packages(),
    include_package_data = True,

    python_requires=">=3.5",
    requires=[],

    author="Sergii Tretiak",
    author_email="tretyak@gmail.com",
    description="Asyncio Influxdb UDP Client",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="LICENSE",
    keywords="udp influx asyncio",
    url = "https://github.com/xmig/udpinflux",

    classifiers=[
        "Development Status :: Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language:: Python:: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database Development"
    ],
)

