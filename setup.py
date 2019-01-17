import os

from setuptools import setup, find_packages

with open('README.md') as readme_fh:
    long_description = readme_fh.read()

with open('requirements.txt') as dependencies_fh:
    dependencies = dependencies_fh.readlines()
    if os.environ.get('ENV') == 'dev':
        with open('requirements-dev.txt') as dev_dependencies_fh:
            dependencies += dev_dependencies_fh.readlines()

setup(
    name='appconstructor',
    version='0.0.0',
    description='Tool to create apps with injected resources',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=dependencies)
