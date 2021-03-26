from setuptools import setup,find_packages
from distutils.cmd import Command
from subprocess import run
from sys import executable

class GenerateDocs(Command):
    user_options=[]

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        run([executable,'-m','pdoc','--docformat','google','-o','docs','matrix'],check=True)

class Publish(Command):
    user_options=[]

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        version:str=[line for line in open('setup.py').readlines() if 'version' in line][-1].strip().replace(' ','')
        version=version[version.find('version=')+9:]
        version=version[:version.find(',')-1]
        print(version)
        changelog:str=input('Write the changelog:')
        #run([executable,'setup.py','bdist_wheel'])


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
    project_urls={'Documentation': 'https://rikyisola.github.io/python-matrix-tuple/'},
    packages=find_packages(),
    cmdclass={'docs':GenerateDocs,'publish':Publish}
)
