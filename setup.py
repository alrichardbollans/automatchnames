from setuptools import setup

# To install run pip install -e PATH_TO_PACKAGE

setup(
    name='automatchnames',
    version='0.0.1',
    packages=['automatchnames','taxa_lists'],
    url='https://github.com/alrichardbollans/automatchnames',
    license='GNU v.3',
    author='Adam Richard-Bollans',
    description='A package for automating name matching of scientific names',
    long_description=open('readme.md',encoding="utf8").read()
)
