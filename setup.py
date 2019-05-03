import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pwned-validator',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Pwned Passwords validator for Django',
    long_description=open('README.rst').read(),
    url='https://github.com/craigloftus/django-pwned-validator',
    author='Craig Loftus',
    author_email='craigloftus@gmail.com',
    python_requires='>=3.5',
    install_requires=[
        'requests',
    ],
    extras_require={
        'test': ['django<2.3', 'pytest', 'pytest-cov', 'pytest-django', 'pytest-vcr',],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
