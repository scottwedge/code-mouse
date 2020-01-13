'''
Build script for setuptools
'''

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='code-mouse-morganecf',
    version='0.0.1',
    author='Morgane Ciot',
    author_email='morganeciot@gmail.com',
    license='MIT',
    description='A tamagotchi mouse that feeds on commits',
    key_words='git hook mouse tamagotchi command line tool cli',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/morganecf/code-mouse/mouse-hook/code-mouse',
    packages=['codemouse'],
    install_requires=[
        'emoji>=0.5.3',
        'colored>=1.4.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['codemouse=codemouse.main:main']
    }
)
