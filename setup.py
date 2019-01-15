from setuptools import setup, find_packages

with open('README.md') as file:
    long_description = file.read()

setup(
    name='appconstructor',
    version='0.0.0',
    description='Tool to create apps with injected resources',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages())
