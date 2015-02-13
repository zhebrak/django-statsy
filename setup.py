# coding: utf-8

from distutils.core import setup

import statsy


setup(
    name='django-statsy',
    packages=['statsy'],
    version=statsy.__version__,
    description='Statistics for Django projects',
    author='Alexander Zhebrak',
    author_email='fata2ex@gmail.com',
    license='MIT',
    url='https://github.com/fata1ex/django-statsy',
    keywords=['django', 'statistics', 'analytics'],
    classifiers=[],
)
