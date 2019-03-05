from __future__ import print_function
from setuptools import setup, find_packages
import parser_engine

setup(
    name="parser_engine",
    version=parser_engine.__version__,
    author="huangzhen",
    author_email="huangzhen@baixing.com",
    description='template parser engine for scrapy',
    long_description=open("README.md").read(),
    license="MIT",
    url="https://gitlab.baixing.cn/spider/parser_engine",
    packages=['parser_engine', 'templates'],
    install_requires=[
        "six",
        "jsonpath-rw",
        "scrapy"
    ],
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
