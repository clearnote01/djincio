import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
name="djinio_pkg",
version="0.0.1",
author="Utkarsh Raj",
author_email="utkarshraj0112@gmail.com",
description="A lightweight layer over some django functions so you can write async code freely",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/clearnote01/djinio",
packages=setuptools.find_packages(),
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],)
