from setuptools import setup,find_packages
from distutils_commands import publish_pypi,publish_github,clean,pytest,command,source,wheel,pdoc,get_cmdclass
from os.path import join

@command('docs')
def docs():
    help(pdoc)
    pdoc('matrix.matrix')


@command('publish')
def publish(changelog:str):
    clean()
    test()
    wheel()
    source()
    publish_github(changelog)
    publish_pypi()
    clean()

@command('test')
def test():
    pytest(join('tests','tests.py'))

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='matrix-tuple',
    version='1.4',
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
    cmdclass=get_cmdclass(),
    provides='matrix',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9'],
    keywords='matrix tuple vector vectors vector2 vector3',
    python_requires='>=3.7',
    setup_requires=['distutils-commands[pdoc]>=1.5.1','distutils-commands[pypi]>=1.5.1',
                    'distutils-commands[pytest]>=1.5.1','distutils-commands[wheel]>=1.5.1','pytest>=6.2.2'],
)
