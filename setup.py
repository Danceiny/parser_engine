import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='parser_engine',
    version='0.0.1',
    scripts=[],
    author="Danceiny",
    author_email="danceiny@gmail.com",
    description="A parser engine born for scrapy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Danceiny/parser_engine",
    packages=setuptools.find_packages(),
    install_requires=[
        'jsonpath-rw',
        'scrapy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
