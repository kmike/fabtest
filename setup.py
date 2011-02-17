#!/usr/bin/env python
from distutils.core import setup

for cmd in ('egg_info', 'develop'):
    import sys
    if cmd in sys.argv:
        from setuptools import setup

version='0.0.5'

setup(
    name='fabtest',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['fabtest'],
    scripts = ['bin/fabtest-preparevm'],
    url='https://bitbucket.org/kmike/fabtest/',
    download_url = 'https://bitbucket.org/kmike/fabtest/get/tip.zip',
    license = 'MIT license',
    description = """ Test Fabric scripts on VirtualBox VMs """,

    long_description = open('README.rst').read(),
    requires = ['Fabric'],

    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ),
)
