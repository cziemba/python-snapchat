from setuptools import setup, find_packages
from os import path

setup(
    name='python-snapchat',

    description='A simple snapchat API',

    version='1.0dev1',

    url='https://github.com/cziemba/python-snapchat',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    packages=find_packages(exclude=['dist', 'tests*']),

    install_requires=['pycrypto'],
)



