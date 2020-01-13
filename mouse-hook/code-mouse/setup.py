'''
Build script for setuptools
'''

## TODO should create $HOME/.codemouse/<datafiles>

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="code-mouse-morganecf",
    version="0.0.1",
    author="Morgane Ciot",
    author_email="morganeciot@gmail.com",
    description="A tamagotchi mouse that feeds on commits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/morganecf/code-mouse/mouse-hook/code-mouse",
    packages=['codemouse'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
