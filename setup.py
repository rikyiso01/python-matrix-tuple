from setuptools import setup,find_packages
from pdoc import pdoc
from pdoc.render import configure
from pathlib import Path
from distutils_commands import publish_pypi,publish_github,clean,pytest,command,source,wheel
from os.path import join

@command
def docs():
    configure(docformat='google')
    pdoc('matrix',output_directory=Path('docs'))

@command
def publish():
    test()
    docs()
    wheel()
    source()
    publish_github()
    publish_pypi()
    clean()

@command
def test():
    pytest(join('tests','tests.py'))

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='matrix-tuple',
    version='1.1',
    description='A python matrix implementation with tuple',
    license="GPL-3",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Riccardo Isola',
    author_email='riky.isola@gmail.com',
    url="https://github.com/RikyIsola/python-matrix-tuple",
    project_urls={
        'Documentation': 'https://rikyisola.github.io/python-matrix-tuple/matrix/matrix.html',
        'Tracker':'https://github.com/RikyIsola/python-matrix-tuple/issues'},
    packages=find_packages(),
    cmdclass={'docs':docs,'publish':publish,'test':test},
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3.9'],
    keywords='matrix tuple vector vectors vector2 vector3',
    python_requires='>=3.9',
)
