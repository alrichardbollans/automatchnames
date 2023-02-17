from setuptools import setup, find_packages

setup(
    name='automatchnames',
    version='DEVX',
    packages=find_packages(),
    install_requires=[
        'pandas==1.4.1',
        'numpy~=1.22.1',
        'requests~=2.27.1',
        'tqdm~=4.62.3',
        'typing~=3.7.4.3'

    ],
    url='https://github.com/alrichardbollans/automatchnames',
    license='GNU v.3',
    author='Adam Richard-Bollans',
    description='A package for downloading WCVP and matching names to it',
    long_description=open('readme.md', encoding="utf8").read()
)
