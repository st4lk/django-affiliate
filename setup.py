import os
import sys
from setuptools import setup, find_packages
from affiliate import __author__, __version__


def __read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

if sys.argv[-1] == 'publish':
    os.system('pandoc --from=markdown --to=rst --output=README.rst README.md')
    os.system('pandoc --from=markdown --to=rst --output=HISTORY.rst HISTORY.md')
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'generate_rst':
    os.system('pandoc --from=markdown --to=rst --output=README.rst README.md')
    os.system('pandoc --from=markdown --to=rst --output=HISTORY.rst HISTORY.md')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a v%s -m 'version %s'" % (__version__, __version__))
    os.system("git push --tags")
    sys.exit()


install_requires = __read('requirements.txt').split()

setup(
    name='django-affiliate',
    author=__author__,
    author_email='alexevseev@gmail.com',
    version=__version__,
    description='Affiliate system for django',
    long_description=__read('README.rst') + '\n\n' + __read('HISTORY.rst'),
    platforms=('Any'),
    packages=find_packages(),
    install_requires=install_requires,
    keywords='django affiliate urls track'.split(),
    include_package_data=True,
    license='BSD License',
    package_dir={'affiliate': 'affiliate'},
    url='https://github.com/st4lk/django-affiliate',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
