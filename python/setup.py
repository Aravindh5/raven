# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='raven',
    version='0.0.1',
    description='Transfer DSA course data to c360',
    long_description=readme,
    author='Valtanix Inc.',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

