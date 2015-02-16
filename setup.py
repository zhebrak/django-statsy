# coding: utf-8

from distutils.core import setup


__version__ = '0.0.6dev'

install_requires = [
    'Django==1.7.4',
    'jsonfield==1.0.2'
]

setup(
    name='django-statsy',
    packages=['statsy'],
    version=__version__,
    description='Statistics for Django projects',
    author='Alexander Zhebrak',
    author_email='fata2ex@gmail.com',
    license='MIT',
    url='https://github.com/fata1ex/django-statsy',
    download_url='https://pypi.python.org/pypi/django-statsy',
    keywords=['django', 'statistics', 'analytics'],
    install_requires=install_requires,
    zip_safe=False,
    include_package_data=True,
    classifiers=[],
)
