# coding: utf-8

from distutils.core import setup

__version__ = '0.1dev'


setup(
    name='django-statsy',
    packages=['statsy'],
    version=__version__,
    description='Statistics for Django projects',
    author='Alexander Zhebrak',
    author_email='fata2ex@gmail.com',
    license='MIT',
    url='https://github.com/fata1ex/django-statsy',
    keywords=['django', 'statistics', 'analytics'],
    classifiers=[],
)
