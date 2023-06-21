from setuptools import setup, find_packages

setup(
    name='automatchnames',
    version='1.2.1',
    packages=find_packages(),
    package_data={"wcvp_download": ["inputs/*"]},
    install_requires=[
        'pandas==2.0.1',
        'numpy==1.24.2',
        'requests==2.31.0',
        'tqdm==4.64.1',
        'typing',
        'zstandard'
    ],
    url='https://github.com/alrichardbollans/automatchnames',
    license='GNU v.3',
    author='Adam Richard-Bollans',
    description='A package for downloading WCVP and matching names to it',
    long_description=open('readme.md', encoding="utf8").read()
)
