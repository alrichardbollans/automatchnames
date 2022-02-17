from setuptools import setup

# To install run pip install -e PATH_TO_PACKAGE

setup(
    name='automatchnames',
    version='0.0.1',
    packages=['unit_tests'],
    url='https://github.com/alrichardbollans/automatchnames',
    license='GNU v.3',
    author='Adam Richard-Bollans',
    author_email='adamrb@protonmail.com',
    description='A package for automating name matching of scientific names',
    long_description=open('README.md').read()
)
