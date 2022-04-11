from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open('README.md', 'r', encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '1.0.6'
DESCRIPTION = "Tinder API - You don't need to hold your phone anymore to submit tinder likes"
# LONG_DESCRIPTION = 'A package that allows get metadata from websites allowing to perfect your targeting.'

# Setting up
setup(
    name="tinderapi",
    version=VERSION,
    author="Aymane Elhattab",
    author_email="<aymane.elhattab.master@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['tinder', 'tinder client', 'bot', 'api'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)