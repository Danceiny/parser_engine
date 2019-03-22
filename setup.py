from __future__ import print_function
from setuptools import setup, find_packages

with open('VERSION') as f:
    __version__ = f.read()
setup(
    name="parser_engine",
    version=__version__,
    author="huangzhen",
    author_email="huangzhen@baixing.com",
    description='template-driven parser engine for scrapy',
    long_description=open("README.md").read(),
    license="MIT",
    url="https://gitlab.baixing.cn/spider/parser_engine",
    packages=find_packages(),
    install_requires=[
        "six",
        "simplejson",
        "jsonpath-rw",
        "scrapy",
        "scrapy_redis",
        "peewee"
    ],
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # 'Natural Language :: Chinese',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Multimedia :: Video',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=True,
)
