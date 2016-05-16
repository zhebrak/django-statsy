# coding: utf-8

from distutils.core import setup


__version__ = '0.1.9'

short_description = 'Statistics for Django projects'

try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = short_description


install_requires = [
    'Django>=1.7',
    'jsonfield>=1.0.0'
]

setup(
    name='django-statsy',
    packages=['statsy'],
    version=__version__,
    description=short_description,
    long_description=long_description,
    author='Alexander Zhebrak',
    author_email='fata2ex@gmail.com',
    license='MIT',
    url='https://github.com/zhebrak/django-statsy',
    download_url='https://pypi.python.org/pypi/django-statsy',
    keywords=['django', 'statistics', 'analytics'],
    install_requires=install_requires,
    zip_safe=False,
    include_package_data=True,
    classifiers=[],
)
