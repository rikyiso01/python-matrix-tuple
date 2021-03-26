from setuptools import setup,find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='matrix-tuple',
    version='1.0',
    description='A python matrix implementation with tuple',
    license="GPL-3",
    long_description=long_description,
    author='Riccardo Isola',
    author_email='riky.isola@gmail.com',
    url="https://github.com/RikyIsola/python-matrix-tuple",
    packages=find_packages,
)
